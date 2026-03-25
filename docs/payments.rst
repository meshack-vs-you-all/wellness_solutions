Payments Module
==============

Overview
--------

The Payments module provides a comprehensive system for processing, tracking, and managing all financial transactions within the Wellness Solutions platform. It handles payment processing, invoicing, refunds, and financial reporting for various entities including clients, instructors, and organizations.

Core Features
------------

* **Secure Payment Processing**: Integration with industry-standard payment gateways
* **Multiple Payment Methods**: Support for credit cards, ACH transfers, and digital wallets
* **Automatic Invoicing**: Generation and delivery of professional invoices
* **Subscription Management**: Handling of recurring payments and memberships
* **Refund Processing**: Full and partial refund capabilities with approval workflows
* **Payment Tracking**: Comprehensive logging of all financial transactions
* **Financial Reporting**: Detailed reports for accounting and financial analysis
* **Tax Management**: Automated tax calculation and reporting
* **Currency Support**: Multi-currency transactions and automatic conversion

Data Models
----------

Payment Model
~~~~~~~~~~~

The base model for tracking financial transactions:

.. code-block:: python

    class Payment(TimeStampedModel):
        """Model for tracking financial transactions."""
        
        PAYMENT_TYPES = [
            ('booking', _('Booking Payment')),
            ('package', _('Package Purchase')),
            ('membership', _('Membership Fee')),
            ('deposit', _('Deposit')),
            ('refund', _('Refund')),
            ('adjustment', _('Adjustment')),
            ('other', _('Other')),
        ]
        
        PAYMENT_STATUSES = [
            ('pending', _('Pending')),
            ('processing', _('Processing')),
            ('completed', _('Completed')),
            ('failed', _('Failed')),
            ('refunded', _('Refunded')),
            ('partially_refunded', _('Partially Refunded')),
            ('cancelled', _('Cancelled')),
        ]
        
        PAYMENT_METHODS = [
            ('credit_card', _('Credit Card')),
            ('ach', _('ACH Transfer')),
            ('bank_transfer', _('Bank Transfer')),
            ('cash', _('Cash')),
            ('check', _('Check')),
            ('digital_wallet', _('Digital Wallet')),
            ('other', _('Other')),
        ]
        
        # Basic information
        payment_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        currency = models.CharField(max_length=3, default='USD')
        payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
        payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
        status = models.CharField(max_length=20, choices=PAYMENT_STATUSES, default='pending')
        
        # Relations
        user = models.ForeignKey(
            'users.User',
            on_delete=models.PROTECT,
            related_name='payments',
            null=True,
            blank=True
        )
        organization = models.ForeignKey(
            'services.Organization',
            on_delete=models.PROTECT,
            related_name='payments',
            null=True,
            blank=True
        )
        
        # Content type for generic relation to a booking, package, etc.
        content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
        object_id = models.PositiveIntegerField(null=True, blank=True)
        content_object = GenericForeignKey('content_type', 'object_id')
        
        # Payment details
        description = models.CharField(max_length=255)
        notes = models.TextField(blank=True)
        transaction_id = models.CharField(max_length=255, blank=True)
        gateway_reference = models.CharField(max_length=255, blank=True)
        
        # Dates
        payment_date = models.DateTimeField(null=True, blank=True)
        due_date = models.DateField(null=True, blank=True)
        
        # Tax information
        tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
        tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        
        # Receipt information
        receipt_number = models.CharField(max_length=50, blank=True)
        receipt_sent = models.BooleanField(default=False)
        
        class Meta:
            verbose_name = _('Payment')
            verbose_name_plural = _('Payments')
            ordering = ['-created']
            
        def __str__(self):
            return f"{self.payment_id} - {self.amount} {self.currency}"
            
        def save(self, *args, **kwargs):
            # Calculate tax amount if not explicitly set
            if self.tax_rate > 0 and self.tax_amount == 0:
                self.tax_amount = self.amount * (self.tax_rate / Decimal('100.0'))
                
            # Set payment date when status changes to completed
            if self.status == 'completed' and not self.payment_date:
                self.payment_date = timezone.now()
                
            # Generate receipt number if payment completed and doesn't have one
            if self.status == 'completed' and not self.receipt_number:
                self.receipt_number = f"REC-{self.payment_id.hex[:8].upper()}"
                
            super().save(*args, **kwargs)
            
        def get_total_amount(self):
            """Get total amount including tax."""
            return self.amount + self.tax_amount
            
        def process_payment(self, gateway_handler=None):
            """Process payment through the appropriate payment gateway."""
            try:
                # Default to system's configured gateway if none provided
                gateway = gateway_handler or PaymentGatewayManager.get_default_gateway()
                
                # Update status to processing
                self.status = 'processing'
                self.save()
                
                # Process payment through gateway
                result = gateway.process_payment(self)
                
                if result.get('success', False):
                    self.status = 'completed'
                    self.transaction_id = result.get('transaction_id', '')
                    self.gateway_reference = result.get('reference', '')
                    self.payment_date = timezone.now()
                    self.save()
                    
                    # Send receipt
                    self.send_receipt()
                    
                    return True, 'Payment processed successfully'
                else:
                    self.status = 'failed'
                    self.notes = f"Payment failed: {result.get('error_message', 'Unknown error')}"
                    self.save()
                    
                    return False, result.get('error_message', 'Payment processing failed')
                    
            except Exception as e:
                self.status = 'failed'
                self.notes = f"Payment processing error: {str(e)}"
                self.save()
                
                return False, str(e)

Invoice Model
~~~~~~~~~~~

For generating and tracking invoices:

.. code-block:: python

    class Invoice(TimeStampedModel):
        """Model for generating and tracking invoices."""
        
        INVOICE_STATUSES = [
            ('draft', _('Draft')),
            ('sent', _('Sent')),
            ('paid', _('Paid')),
            ('partially_paid', _('Partially Paid')),
            ('overdue', _('Overdue')),
            ('cancelled', _('Cancelled')),
        ]
        
        # Basic information
        invoice_number = models.CharField(max_length=50, unique=True)
        status = models.CharField(max_length=20, choices=INVOICE_STATUSES, default='draft')
        
        # Relations
        user = models.ForeignKey(
            'users.User',
            on_delete=models.PROTECT,
            related_name='invoices',
            null=True,
            blank=True
        )
        organization = models.ForeignKey(
            'services.Organization',
            on_delete=models.PROTECT,
            related_name='invoices',
            null=True,
            blank=True
        )
        
        # Billing information
        billing_name = models.CharField(max_length=255)
        billing_address = models.TextField()
        billing_email = models.EmailField()
        billing_phone = models.CharField(max_length=20, blank=True)
        
        # Dates
        issue_date = models.DateField()
        due_date = models.DateField()
        
        # Amounts
        subtotal = models.DecimalField(max_digits=10, decimal_places=2)
        tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        total_amount = models.DecimalField(max_digits=10, decimal_places=2)
        amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        
        # Additional information
        notes = models.TextField(blank=True)
        terms = models.TextField(blank=True)
        
        class Meta:
            verbose_name = _('Invoice')
            verbose_name_plural = _('Invoices')
            ordering = ['-issue_date']
            
        def __str__(self):
            return self.invoice_number
            
        def get_balance_due(self):
            """Get remaining balance due on this invoice."""
            return self.total_amount - self.amount_paid
            
        def is_overdue(self):
            """Check if invoice is overdue."""
            return self.due_date < timezone.now().date() and self.status not in ['paid', 'cancelled']
            
        def update_status(self):
            """Update invoice status based on payments."""
            balance = self.get_balance_due()
            
            if balance <= 0:
                self.status = 'paid'
            elif self.amount_paid > 0:
                self.status = 'partially_paid'
            elif self.is_overdue():
                self.status = 'overdue'
                
            self.save()
            
        def generate_pdf(self):
            """Generate PDF version of invoice."""
            # Implementation of PDF generation
            from .utils.invoice_generator import generate_invoice_pdf
            return generate_invoice_pdf(self)
            
        def send_invoice(self, recipient_email=None):
            """Send invoice to client."""
            email = recipient_email or self.billing_email
            
            # Generate PDF
            pdf_file = self.generate_pdf()
            
            # Send email with PDF attachment
            subject = f"Invoice {self.invoice_number} from Wellness Solutions"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email]
            
            # Email content
            context = {
                'invoice': self,
                'client_name': self.billing_name,
                'due_date': self.due_date,
                'amount': self.total_amount,
            }
            
            # Send email
            send_invoice_email(subject, from_email, to_email, context, pdf_file)
            
            # Update status if it was in draft
            if self.status == 'draft':
                self.status = 'sent'
                self.save()
                
            return True

InvoiceItem Model
~~~~~~~~~~~~~~

For tracking individual items on an invoice:

.. code-block:: python

    class InvoiceItem(TimeStampedModel):
        """Model for individual items on an invoice."""
        
        invoice = models.ForeignKey(
            Invoice,
            on_delete=models.CASCADE,
            related_name='items'
        )
        
        description = models.CharField(max_length=255)
        quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
        unit_price = models.DecimalField(max_digits=10, decimal_places=2)
        tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
        discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
        
        # Content type for generic relation to a booking, package, etc.
        content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
        object_id = models.PositiveIntegerField(null=True, blank=True)
        content_object = GenericForeignKey('content_type', 'object_id')
        
        class Meta:
            verbose_name = _('Invoice Item')
            verbose_name_plural = _('Invoice Items')
            
        def __str__(self):
            return f"{self.invoice.invoice_number} - {self.description}"
            
        def get_subtotal(self):
            """Calculate subtotal for this item (quantity * unit_price)."""
            return self.quantity * self.unit_price
            
        def get_tax_amount(self):
            """Calculate tax amount for this item."""
            return self.get_subtotal() * (self.tax_rate / Decimal('100.0'))
            
        def get_total(self):
            """Calculate total for this item including tax and discount."""
            subtotal = self.get_subtotal()
            tax = self.get_tax_amount()
            return subtotal + tax - self.discount_amount

Payment Gateway Integration
--------------------------

The module provides a unified interface for multiple payment gateways:

.. code-block:: python

    class PaymentGatewayManager:
        """Manager class for payment gateways."""
        
        @classmethod
        def get_gateway(cls, gateway_name):
            """Get payment gateway handler by name."""
            gateways = {
                'stripe': StripeGateway,
                'paypal': PayPalGateway,
                'authorize': AuthorizeNetGateway,
                'square': SquareGateway,
                'manual': ManualGateway,
            }
            
            return gateways.get(gateway_name.lower(), ManualGateway)()
            
        @classmethod
        def get_default_gateway(cls):
            """Get the default payment gateway based on settings."""
            default = getattr(settings, 'DEFAULT_PAYMENT_GATEWAY', 'stripe')
            return cls.get_gateway(default)
            
        @classmethod
        def process_payment(cls, payment, gateway_name=None):
            """Process a payment through the specified gateway."""
            gateway = (
                cls.get_gateway(gateway_name) if gateway_name
                else cls.get_default_gateway()
            )
            
            return gateway.process_payment(payment)

API Endpoints
------------

Payment Management
~~~~~~~~~~~~~~~~

**GET** ``/api/payments/``

* Lists payments with filtering options
* Parameters:
  * ``user_id`` - Filter by user ID
  * ``organization_id`` - Filter by organization ID
  * ``status`` - Filter by payment status
  * ``payment_type`` - Filter by payment type
  * ``start_date`` - Filter by date range start
  * ``end_date`` - Filter by date range end

**POST** ``/api/payments/``

* Creates a new payment
* Required fields:
  * ``amount`` - Payment amount
  * ``currency`` - Currency code (default: USD)
  * ``payment_type`` - Type of payment
  * ``payment_method`` - Method of payment
  * ``description`` - Payment description
* Optional fields:
  * ``user`` - User ID (if applicable)
  * ``organization`` - Organization ID (if applicable)
  * ``content_type`` and ``object_id`` - For generic relation
  * ``notes`` - Additional notes
  * ``due_date`` - Payment due date

**GET** ``/api/payments/{id}/``

* Returns detailed information about a specific payment
* Includes complete payment history and related transaction data

**PATCH** ``/api/payments/{id}/``

* Updates payment information (limited fields)
* Restricted based on payment status and user role

Payment Processing
~~~~~~~~~~~~~~~~

**POST** ``/api/payments/process/``

* Processes a payment through the configured gateway
* Required fields:
  * ``payment_id`` - ID of the payment to process
  * ``payment_method_id`` - ID of the saved payment method or token
* Optional fields:
  * ``gateway`` - Specific gateway to use (defaults to system configuration)
  * ``save_payment_method`` - Whether to save the payment method for future use

**POST** ``/api/payments/{id}/refund/``

* Processes a refund for a payment
* Required fields:
  * ``amount`` - Amount to refund (for partial refunds)
* Optional fields:
  * ``reason`` - Reason for the refund
  * ``notify_customer`` - Whether to notify the customer about the refund

Invoice Management
~~~~~~~~~~~~~~~~

**GET** ``/api/invoices/``

* Lists invoices with filtering options
* Parameters:
  * ``user_id`` - Filter by user ID
  * ``organization_id`` - Filter by organization ID
  * ``status`` - Filter by invoice status
  * ``start_date`` - Filter by date range start
  * ``end_date`` - Filter by date range end

**POST** ``/api/invoices/``

* Creates a new invoice
* Required fields:
  * ``billing_name`` - Name for billing
  * ``billing_address`` - Address for billing
  * ``billing_email`` - Email for billing
  * ``issue_date`` - Invoice issue date
  * ``due_date`` - Invoice due date
  * ``items`` - Array of invoice items with description, quantity, and unit price
* Optional fields:
  * ``user`` - User ID (if applicable)
  * ``organization`` - Organization ID (if applicable)
  * ``notes`` - Additional invoice notes
  * ``terms`` - Invoice terms and conditions

**GET** ``/api/invoices/{id}/``

* Returns detailed information about a specific invoice
* Includes all invoice items and payment history

**POST** ``/api/invoices/{id}/send/``

* Sends the invoice to the specified recipient
* Optional fields:
  * ``recipient_email`` - Alternative email address to send to
  * ``include_payment_link`` - Whether to include payment link in the email

**GET** ``/api/invoices/{id}/pdf/``

* Generates and returns a PDF version of the invoice

Payment Methods
~~~~~~~~~~~~~

**GET** ``/api/payment-methods/``

* Lists saved payment methods for the authenticated user
* Includes card type, last four digits, and expiration date for cards

**POST** ``/api/payment-methods/``

* Saves a new payment method
* Required fields:
  * ``token`` - Secure token from payment gateway
  * ``payment_method_type`` - Type of payment method
* Optional fields:
  * ``is_default`` - Whether this is the default payment method
  * ``nickname`` - User-friendly name for the payment method

**DELETE** ``/api/payment-methods/{id}/``

* Removes a saved payment method

Integration Points
-----------------

* **Users Module**: Payment attribution and customer management
* **Bookings Module**: Payment for individual sessions and classes
* **Packages Module**: Purchase and management of multi-session packages
* **Organizations Module**: Corporate billing and invoicing
* **Reporting Module**: Financial data for reports and analytics

Best Practices
-------------

1. **Payment Security**
   * Never store sensitive card data directly in the database
   * Use tokenization for all payment methods
   * Implement proper encryption for all financial data
   * Follow PCI-DSS compliance requirements

2. **Transaction Management**
   * Always use atomic operations for payment processing
   * Implement robust error handling and recovery
   * Maintain comprehensive transaction logs
   * Include idempotency keys to prevent duplicate transactions

3. **Invoicing Guidelines**
   * Include clear payment terms on all invoices
   * Set reasonable due dates based on client relationships
   * Include detailed line items and tax information
   * Provide multiple payment options when possible

4. **Refund Policies**
   * Document clear refund policies for different payment types
   * Implement proper approval workflows for refunds
   * Maintain audit trail for all refund transactions
   * Consider partial refund options where appropriate

5. **Financial Reconciliation**
   * Regularly reconcile payment records with gateway reports
   * Implement automated detection of payment discrepancies
   * Maintain historical records for financial auditing
   * Create regular financial reports for accounting purposes

Example Usage
------------

Processing a Booking Payment
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def process_booking_payment(booking, payment_method_id, user):
        """Process payment for a booking."""
        # Create payment record
        payment = Payment.objects.create(
            amount=booking.total_price,
            currency='USD',
            payment_type='booking',
            payment_method='credit_card',
            user=user,
            content_type=ContentType.objects.get_for_model(Booking),
            object_id=booking.id,
            description=f"Payment for booking #{booking.booking_reference}",
            due_date=timezone.now().date()
        )
        
        # Process payment through gateway
        gateway = PaymentGatewayManager.get_default_gateway()
        result = gateway.process_payment(
            payment=payment,
            payment_method_id=payment_method_id,
            customer_id=user.customer_profile_id
        )
        
        if result.get('success', False):
            # Update booking status
            booking.payment_status = 'paid'
            booking.status = 'confirmed'
            booking.save()
            
            # Record payment details
            payment.status = 'completed'
            payment.transaction_id = result.get('transaction_id')
            payment.gateway_reference = result.get('reference')
            payment.payment_date = timezone.now()
            payment.save()
            
            # Send confirmation
            send_booking_confirmation(booking)
            
            return True, payment
        else:
            # Handle payment failure
            payment.status = 'failed'
            payment.notes = f"Payment failed: {result.get('error_message', 'Unknown error')}"
            payment.save()
            
            return False, result.get('error_message', 'Payment processing failed')

Generating an Invoice
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def generate_organization_invoice(organization, items, due_days=30):
        """Generate an invoice for an organization."""
        # Generate invoice number
        prefix = "INV"
        current_date = timezone.now().date()
        date_string = current_date.strftime("%Y%m")
        count = Invoice.objects.filter(
            invoice_number__startswith=f"{prefix}-{date_string}"
        ).count() + 1
        
        invoice_number = f"{prefix}-{date_string}-{count:04d}"
        
        # Calculate totals
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
        tax_amount = Decimal('0.00')
        discount_amount = Decimal('0.00')
        
        # Apply tax if necessary
        tax_rate = organization.tax_rate or Decimal('0.00')
        if tax_rate > 0:
            tax_amount = subtotal * (tax_rate / Decimal('100.0'))
            
        # Calculate total
        total_amount = subtotal + tax_amount - discount_amount
        
        # Create invoice
        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            organization=organization,
            billing_name=organization.name,
            billing_address=organization.address,
            billing_email=organization.contact_email,
            billing_phone=organization.contact_phone,
            issue_date=current_date,
            due_date=current_date + timedelta(days=due_days),
            subtotal=subtotal,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            total_amount=total_amount,
            notes=f"Monthly invoice for {current_date.strftime('%B %Y')}",
            terms="Payment due within 30 days of invoice date."
        )
        
        # Create invoice items
        for item in items:
            InvoiceItem.objects.create(
                invoice=invoice,
                description=item['description'],
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                tax_rate=tax_rate,
                content_type=item.get('content_type'),
                object_id=item.get('object_id')
            )
            
        return invoice
