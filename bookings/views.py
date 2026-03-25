"""
Views for the bookings app.
"""

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from services.models import Service

from .forms import BookingCancellationForm, BookingForm, BookingPaymentForm
from .models import Booking, BookingStatus, PaymentStatus


User = get_user_model()


class BookingListView(LoginRequiredMixin, ListView):
    """List all bookings."""

    model = Booking
    context_object_name = "bookings"
    template_name = "bookings/booking_list.html"
    paginate_by = 20

    def get_queryset(self):
        """Filter bookings based on user permissions."""
        queryset = super().get_queryset()

        if not self.request.user.is_staff:
            # Regular users only see their own bookings
            queryset = queryset.filter(client=self.request.user)

        # Add filters based on query parameters
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)

        date_from = self.request.GET.get("date_from")
        if date_from:
            queryset = queryset.filter(start_time__date__gte=date_from)

        date_to = self.request.GET.get("date_to")
        if date_to:
            queryset = queryset.filter(start_time__date__lte=date_to)

        return queryset.select_related(
            "client", "location", "service", "instructor",
        )

    def get_context_data(self, **kwargs):
        """Add extra context for the template."""
        context = super().get_context_data(**kwargs)
        context["booking_statuses"] = BookingStatus.choices
        return context


class BookingDetailView(LoginRequiredMixin, DetailView):
    """Display booking details."""

    model = Booking
    context_object_name = "booking"
    template_name = "bookings/booking_detail.html"

    def get_queryset(self):
        """Ensure users can only view their own bookings unless staff."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(client=self.request.user)
        return queryset.select_related(
            "client", "location", "service", "instructor",
            "cancellation",
        ).prefetch_related("payments")


class BookingCreateView(LoginRequiredMixin, CreateView):
    """Create a new booking."""

    model = Booking
    form_class = BookingForm
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy("bookings:booking-list")

    def get_context_data(self, **kwargs):
        """Add extra context for the booking form."""
        context = super().get_context_data(**kwargs)

        # Add available services
        context["services"] = Service.objects.filter(active=True).annotate(
            rating=Avg("instructor__reviews__rating"),
            review_count=Count("instructor__reviews"),
        )

        # Add available instructors
        context["instructors"] = User.objects.filter(
            is_active=True,
            wellness_instructor__isnull=False,
        ).annotate(
            rating=Avg("wellness_instructor__reviews__rating"),
            review_count=Count("wellness_instructor__reviews"),
        )

        # Add date range
        today = timezone.now().date()
        context["min_date"] = today
        context["max_date"] = today + timedelta(days=30)  # Allow booking up to 30 days ahead

        # Add time slots
        if self.request.GET.get("date"):
            date = parse_date(self.request.GET["date"])
            instructor_id = self.request.GET.get("instructor")

            if date and instructor_id:
                context["time_slots"] = self.get_available_time_slots(date, instructor_id)

        return context

    def get_available_time_slots(self, date, instructor_id):
        """Get available time slots for the given date and instructor."""
        instructor = get_object_or_404(User, id=instructor_id)

        # Get instructor's schedule for the day
        schedule = instructor.wellness_instructor.schedule_set.filter(
            day_of_week=date.weekday(),
        ).first()

        if not schedule:
            return []

        # Get all existing bookings for the instructor on this date
        existing_bookings = Booking.objects.filter(
            instructor=instructor,
            start_time__date=date,
        ).values_list("start_time", "end_time")

        # Generate time slots
        slots = []
        current_time = timezone.make_aware(datetime.combine(date, schedule.start_time))
        end_time = timezone.make_aware(datetime.combine(date, schedule.end_time))

        while current_time + timedelta(minutes=60) <= end_time:
            slot_end = current_time + timedelta(minutes=60)

            # Check if slot conflicts with existing bookings
            is_available = True
            for booking_start, booking_end in existing_bookings:
                if (current_time >= booking_start and current_time < booking_end) or \
                   (slot_end > booking_start and slot_end <= booking_end):
                    is_available = False
                    break

            if is_available:
                slots.append({
                    "id": current_time.strftime("%H:%M"),
                    "start_time": current_time.time(),
                    "end_time": slot_end.time(),
                })

            current_time = slot_end

        return slots

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def validate_booking(self, form):
        """Validate booking data."""
        cleaned_data = form.cleaned_data
        errors = []

        try:
            # Validate booking time
            validate_booking_time(
                cleaned_data["start_time"],
                cleaned_data["service"],
            )

            # Validate instructor availability
            validate_instructor_availability(
                cleaned_data["instructor"],
                cleaned_data["start_time"],
                cleaned_data["service"],
            )

            # Validate client eligibility
            validate_client_eligibility(
                self.request.user,
                cleaned_data["service"],
                cleaned_data["start_time"],
            )

        except ValidationError as e:
            errors.extend(e.messages)

        return errors

    @transaction.atomic
    def form_valid(self, form):
        """Process the valid form data."""
        try:
            with transaction.atomic():
                # Lock the instructor record to prevent race conditions
                instructor = form.cleaned_data["instructor"]
                # We use select_for_update() here to ensure no other booking can be made 
                # for this instructor simultaneously until this transaction completes.
                LocationInstructor.objects.select_for_update().get(pk=instructor.pk)

                # Validate booking within the locked transaction
                errors = self.validate_booking(form)
                if errors:
                    for error in errors:
                        form.add_error(None, error)
                    return self.form_invalid(form)

                # Set the client
                form.instance.client = self.request.user

                # Calculate total amount
                service = form.cleaned_data["service"]
                form.instance.total_amount = service.calculate_total_price()

                # Save the booking
                response = super().form_valid(form)

                # Send confirmation
                from .utils import send_booking_confirmation
                send_booking_confirmation(self.object)

                messages.success(
                    self.request,
                    _("Booking created successfully!"),
                )

                return response

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class BookingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing booking."""

    model = Booking
    form_class = BookingForm
    template_name = "bookings/booking_form.html"
    success_url = reverse_lazy("bookings:booking-list")

    def test_func(self):
        """Check if user can update the booking."""
        booking = self.get_object()
        return (
            self.request.user.is_staff or
            booking.client == self.request.user
        )

    def get_form_kwargs(self):
        """Pass the current user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def validate_booking_update(self, form, booking):
        """Validate booking update data."""
        cleaned_data = form.cleaned_data
        errors = []

        try:
            # Validate booking time for updates
            if cleaned_data["start_time"] != booking.start_time:
                validate_booking_time(
                    cleaned_data["start_time"],
                    cleaned_data["service"],
                )

            # Validate instructor availability for updates
            if (cleaned_data["start_time"] != booking.start_time or
                cleaned_data["instructor"] != booking.instructor):
                validate_instructor_availability(
                    cleaned_data["instructor"],
                    cleaned_data["start_time"],
                    cleaned_data["service"],
                )

            # Validate client eligibility for updates
            if cleaned_data["service"] != booking.service:
                validate_client_eligibility(
                    self.request.user,
                    cleaned_data["service"],
                    cleaned_data["start_time"],
                )

        except ValidationError as e:
            errors.extend(e.messages)

        return errors

    @transaction.atomic
    def form_valid(self, form):
        """Process the valid form data."""
        booking = self.get_object()

        # Validate booking update
        errors = self.validate_booking_update(form, booking)
        if errors:
            for error in errors:
                form.add_error(None, error)
            return self.form_invalid(form)

        try:
            with transaction.atomic():
                # Update total amount if service changed
                service = form.cleaned_data["service"]
                if service != booking.service:
                    form.instance.total_amount = service.calculate_total_price()

                # Save the booking
                response = super().form_valid(form)

                messages.success(
                    self.request,
                    _("Booking updated successfully!"),
                )

                return response

        except Exception as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)


class BookingCancelView(LoginRequiredMixin, UserPassesTestMixin, SingleObjectMixin, FormView):
    """Cancel a booking."""

    model = Booking
    form_class = BookingCancellationForm
    template_name = "bookings/booking_cancel.html"
    success_url = reverse_lazy("bookings:booking-list")

    def test_func(self):
        """Check if user can cancel the booking."""
        booking = self.get_object()
        return (
            self.request.user.is_staff or
            (booking.client == self.request.user and booking.can_be_cancelled())
        )

    def get_form_kwargs(self):
        """Pass the booking to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["booking"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        """Process the cancellation."""
        booking = self.get_object()
        with transaction.atomic():
            # Create cancellation record
            cancellation = form.save(commit=False)
            cancellation.booking = booking
            cancellation.cancelled_by = self.request.user
            cancellation.save()

            # Update booking status
            booking.status = BookingStatus.CANCELLED
            booking.save()

            # Send cancellation email
            send_booking_cancelled(booking)

            messages.success(
                self.request,
                _("Booking cancelled successfully."),
            )

        return super().form_valid(form)


class BookingPaymentView(LoginRequiredMixin, SingleObjectMixin, FormView):
    """Process payment for a booking."""

    model = Booking
    form_class = BookingPaymentForm
    template_name = "bookings/booking_payment.html"

    def get_success_url(self):
        """Return to booking detail page after payment."""
        return reverse_lazy(
            "bookings:booking-detail",
            kwargs={"pk": self.object.pk},
        )

    def get_form_kwargs(self):
        """Pass the booking to the form."""
        kwargs = super().get_form_kwargs()
        kwargs["booking"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        """Process the payment."""
        booking = self.get_object()
        with transaction.atomic():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.payer = self.request.user
            payment.save()

            # Send payment confirmation
            send_payment_confirmation(payment)

            # Update booking payment status
            total_paid = booking.payments.aggregate(
                total=models.Sum("amount"),
            )["total"] or 0

            if total_paid >= booking.total_price:
                booking.payment_status = PaymentStatus.PAID
            elif total_paid > 0:
                booking.payment_status = PaymentStatus.PARTIALLY_PAID
            booking.save()

            messages.success(
                self.request,
                _("Payment processed successfully."),
            )

        return super().form_valid(form)


class CompletedSessionsView(LoginRequiredMixin, ListView):
    """List completed sessions for an instructor."""

    model = Booking
    template_name = "bookings/completed_sessions.html"
    context_object_name = "completed_sessions"
    paginate_by = 20

    def get_queryset(self):
        """Filter completed sessions for the current instructor."""
        return Booking.objects.filter(
            instructor__user=self.request.user,
            status=BookingStatus.COMPLETED,
        ).select_related(
            "client",
            "organization",
            "location",
            "service",
            "instructor",
        ).order_by("-start_time")

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Completed Sessions")
        return context


class UpcomingSessionsView(LoginRequiredMixin, ListView):
    """List upcoming sessions for an instructor."""

    model = Booking
    template_name = "bookings/upcoming_sessions.html"
    context_object_name = "upcoming_sessions"
    paginate_by = 20

    def get_queryset(self):
        """Filter upcoming sessions for the current instructor."""
        now = timezone.now()
        return Booking.objects.filter(
            instructor__user=self.request.user,
            start_time__gte=now,
            status=BookingStatus.CONFIRMED,
        ).select_related(
            "client",
            "organization",
            "location",
            "service",
            "instructor",
        ).order_by("start_time")

    def get_context_data(self, **kwargs):
        """Add extra context."""
        context = super().get_context_data(**kwargs)
        context["title"] = _("Upcoming Sessions")
        return context


class BookingHistoryView(LoginRequiredMixin, ListView):
    template_name = "bookings/booking_history.html"
    context_object_name = "bookings"
    paginate_by = 10

    def get_queryset(self):
        return Booking.objects.filter(
            client=self.request.user,
            status__in=["completed", "cancelled"],
        ).order_by("-created_at")


class InstructorClientListView(LoginRequiredMixin, ListView):
    template_name = "bookings/instructor_client_list.html"
    context_object_name = "clients"
    paginate_by = 20

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "wellness_instructor"):
            return redirect("users:client_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return User.objects.filter(
            booking__instructor=self.request.user.wellness_instructor,
            booking__status="completed",
        ).distinct().order_by("-booking__created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_clients"] = self.get_queryset().count()
        return context


class InstructorClientDetailView(LoginRequiredMixin, DetailView):
    template_name = "bookings/instructor_client_detail.html"
    context_object_name = "client"
    model = User

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "wellness_instructor"):
            return redirect("users:client_dashboard")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.get_object()

        # Get all bookings for this client with this instructor
        bookings = Booking.objects.filter(
            client=client,
            instructor=self.request.user.wellness_instructor,
        ).order_by("-created_at")

        context.update({
            "bookings": bookings,
            "total_sessions": bookings.filter(status="completed").count(),
            "upcoming_sessions": bookings.filter(
                status="confirmed",
                start_time__gt=timezone.now(),
            ),
            "completion_rate": self._calculate_completion_rate(client),
            "attendance_rate": self._calculate_attendance_rate(client),
        })
        return context

    def _calculate_completion_rate(self, client):
        total = Booking.objects.filter(
            client=client,
            instructor=self.request.user.wellness_instructor,
            status__in=["completed", "cancelled"],
        ).count()

        if not total:
            return 0

        completed = Booking.objects.filter(
            client=client,
            instructor=self.request.user.wellness_instructor,
            status="completed",
        ).count()

        return (completed / total) * 100

    def _calculate_attendance_rate(self, client):
        total = Booking.objects.filter(
            client=client,
            instructor=self.request.user.wellness_instructor,
            status__in=["completed", "no_show"],
        ).count()

        if not total:
            return 0

        attended = Booking.objects.filter(
            client=client,
            instructor=self.request.user.wellness_instructor,
            status="completed",
        ).count()

        return (attended / total) * 100


@require_http_methods(["GET"])
def get_time_slots(request):
    """AJAX endpoint to get available time slots."""
    date = request.GET.get("date")
    instructor_id = request.GET.get("instructor")

    if not date or not instructor_id:
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    try:
        date = parse_date(date)
        instructor = get_object_or_404(User, id=instructor_id)

        # Get instructor's schedule for the day
        schedule = instructor.wellness_instructor.schedule_set.filter(
            day_of_week=date.weekday(),
        ).first()

        if not schedule:
            return JsonResponse({"time_slots": []})

        # Get all existing bookings for the instructor on this date
        existing_bookings = Booking.objects.filter(
            instructor=instructor,
            start_time__date=date,
        ).values_list("start_time", "end_time")

        # Generate time slots
        slots = []
        current_time = timezone.make_aware(datetime.combine(date, schedule.start_time))
        end_time = timezone.make_aware(datetime.combine(date, schedule.end_time))

        while current_time + timedelta(minutes=60) <= end_time:
            slot_end = current_time + timedelta(minutes=60)

            # Check if slot conflicts with existing bookings
            is_available = True
            for booking_start, booking_end in existing_bookings:
                if (current_time >= booking_start and current_time < booking_end) or \
                   (slot_end > booking_start and slot_end <= booking_end):
                    is_available = False
                    break

            if is_available:
                slots.append({
                    "id": current_time.strftime("%H:%M"),
                    "start_time": current_time.strftime("%I:%M %p"),
                    "end_time": slot_end.strftime("%I:%M %p"),
                })

            current_time = slot_end

        return JsonResponse({"time_slots": slots})

    except (ValueError, TypeError):
        return JsonResponse({"error": "Invalid parameters"}, status=400)
