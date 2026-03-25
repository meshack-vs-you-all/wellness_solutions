import stripe
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from bookings.models import Booking, PaymentStatus as BookingPaymentStatus
from services.models import ServicePackage
from .models import PaymentTransaction

stripe.api_key = settings.STRIPE_SECRET_KEY

# Flutterwave Initialization
from rave_python import Rave
rave = Rave(settings.FLUTTERWAVE_PUBLIC_KEY, settings.FLUTTERWAVE_SECRET_KEY, production=False)


class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Create a Stripe or Flutterwave Checkout Session for a Booking or ServicePackage.
        Expected data: { "item_type": "booking" | "package", "item_id": 123, "gateway": "stripe" | "flutterwave" }
        """
        item_type = request.data.get("item_type")
        item_id = request.data.get("item_id")
        gateway = request.data.get("gateway", "stripe")

        if not item_type or not item_id:
            return Response(
                {"error": "item_type and item_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if item_type == "booking":
                item = Booking.objects.get(id=item_id, client=request.user)
                name = f"Booking {item.booking_number}"
                amount = float(item.total_price)
                content_type = ContentType.objects.get_for_model(Booking)
            elif item_type == "package":
                item = ServicePackage.objects.get(id=item_id)
                name = f"Package: {item.name}"
                amount = float(item.get_total_price())
                content_type = ContentType.objects.get_for_model(ServicePackage)
            else:
                return Response({"error": "Invalid item_type"}, status=status.HTTP_400_BAD_REQUEST)

            frontend_url = "http://localhost:5173"

            if gateway == "stripe":
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    line_items=[
                        {
                            "price_data": {
                                "currency": settings.STRIPE_CURRENCY,
                                "product_data": {
                                    "name": name,
                                },
                                "unit_amount": int(amount * 100),
                            },
                            "quantity": 1,
                        }
                    ],
                    mode="payment",
                    success_url=f"{frontend_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
                    cancel_url=f"{frontend_url}/payment/cancel",
                    metadata={
                        "item_type": item_type,
                        "item_id": item_id,
                        "user_id": request.user.id,
                    },
                )

                # Save the transaction in our database
                PaymentTransaction.objects.create(
                    user=request.user,
                    content_type=content_type,
                    object_id=item_id,
                    stripe_checkout_session_id=checkout_session.id,
                    amount=amount,
                    currency=settings.STRIPE_CURRENCY,
                    status=PaymentTransaction.Status.PENDING,
                )
                return Response({"checkout_url": checkout_session.url})

            elif gateway == "flutterwave":
                # For Flutterwave (M-Pesa support)
                import uuid
                tx_ref = f"TX-{uuid.uuid4()}"
                
                res = rave.Card.charge({
                    "amount": amount,
                    "email": request.user.email,
                    "phonenumber": getattr(request.user, "phone", ""),
                    "firstname": request.user.first_name,
                    "lastname": request.user.last_name,
                    "tx_ref": tx_ref,
                    "redirect_url": f"{frontend_url}/payment/success",
                    "currency": settings.FLUTTERWAVE_CURRENCY,
                    "payment_options": "card,mpesa",
                    "custom_title": "Wellness Solutions",
                    "custom_description": name,
                })
                
                # Note: Rave's standard checkout is often easier via direct link
                # For simplicity in this demo, we'll return a simulated link or use their Standard flow
                # Re-using the transaction model with tx_ref as session_id for consistency
                PaymentTransaction.objects.create(
                    user=request.user,
                    content_type=content_type,
                    object_id=item_id,
                    stripe_checkout_session_id=tx_ref, # Using tx_ref here
                    amount=amount,
                    currency=settings.FLUTTERWAVE_CURRENCY,
                    status=PaymentTransaction.Status.PENDING,
                )
                
                # In a real scenario, you'd use Flutterwave Standard to get a redirect URL
                return Response({
                    "checkout_url": f"https://checkout.flutterwave.com/v3/hosted/pay",
                    "params": {
                        "public_key": settings.FLUTTERWAVE_PUBLIC_KEY,
                        "tx_ref": tx_ref,
                        "amount": amount,
                        "currency": settings.FLUTTERWAVE_CURRENCY,
                        "redirect_url": f"{frontend_url}/payment/success",
                        "customer": {
                            "email": request.user.email,
                            "name": request.user.get_full_name(),
                        },
                        "customizations": {
                            "title": "Wellness Solutions",
                            "description": name,
                        }
                    }
                })

        except (Booking.DoesNotExist, ServicePackage.DoesNotExist):
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        
        # Update the transaction status
        try:
            transaction = PaymentTransaction.objects.get(stripe_checkout_session_id=session.id)
            transaction.status = PaymentTransaction.Status.COMPLETED
            transaction.stripe_payment_intent_id = session.payment_intent
            transaction.save()
            
            # Update the actual item status
            item = transaction.content_object
            if isinstance(item, Booking):
                item.payment_status = BookingPaymentStatus.PAID
                item.save()
                
                # Also create a BookingPayment record
                from bookings.models import BookingPayment, PaymentMethod
                BookingPayment.objects.create(
                    booking=item,
                    amount=transaction.amount,
                    payment_method=PaymentMethod.CREDIT_CARD,
                    transaction_id=session.id,
                    status=BookingPaymentStatus.PAID,
                    payer=transaction.user,
                )
            elif isinstance(item, ServicePackage):
                # If it's a package purchase, create a Package instance for the user
                from packages.models import Package
                from django.utils import timezone
                Package.objects.create(
                    owner=transaction.user,
                    service_package=item,
                    name=item.name,
                    total_sessions=item.sessions,
                    expiry_date=timezone.now().date() + timezone.timedelta(days=item.validity_days)
                )
                
        except PaymentTransaction.DoesNotExist:
            pass

    return HttpResponse(status=200)
