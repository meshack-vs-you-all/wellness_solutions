Packages Module
==============

Overview
--------

The Packages module provides a flexible system for managing service packages, allowing clients to purchase multiple sessions at discounted rates. It handles package creation, assignment, tracking, and expiration with robust validation rules and integration with the booking system.

Core Features
------------

* **Package Management**: Create and manage service packages with varying session counts
* **Client Assignment**: Assign packages to individual clients or organizations
* **Usage Tracking**: Monitor session usage and remaining balance
* **Expiration Handling**: Automatic expiration based on configurable timeframes
* **Transferability**: Optional ability to transfer packages between clients
* **Pricing Rules**: Flexible discount structures based on quantity
* **Package Types**: Support for individual, group, and corporate packages

Data Models
----------

Package Model
~~~~~~~~~~~~

The primary model for package definition:

.. code-block:: python

    class Package(TimeStampedModel):
        """Model for managing service packages."""
        
        name = models.CharField(max_length=100)
        description = models.TextField(blank=True)
        service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
        
        # Package details
        total_sessions = models.PositiveIntegerField(validators=[MinValueValidator(1)])
        sessions_remaining = models.PositiveIntegerField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        per_session_price = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Validity
        purchase_date = models.DateField(default=timezone.now)
        expiry_date = models.DateField()
        active = models.BooleanField(default=True)
        
        # Ownership
        owner = models.ForeignKey('users.User', on_delete=models.CASCADE)
        transferable = models.BooleanField(default=False)
        
        # For corporate packages
        organization = models.ForeignKey(
            'services.Organization',
            on_delete=models.SET_NULL,
            null=True,
            blank=True
        )

Key validation rules:
* Total sessions must be positive
* Sessions remaining cannot exceed total sessions
* Expiry date must be after purchase date
* Per-session price must be less than or equal to the standard service price

ClientPackage Model
~~~~~~~~~~~~~~~~~

For tracking package assignments to clients:

.. code-block:: python

    class ClientPackageAssignment(TimeStampedModel):
        """Model for tracking package assignments to clients."""
        
        package = models.ForeignKey(
            Package, 
            on_delete=models.CASCADE,
            related_name='client_assignments'
        )
        client = models.ForeignKey(
            'users.User',
            on_delete=models.CASCADE,
            related_name='assigned_packages'
        )
        sessions_allocated = models.PositiveIntegerField()
        sessions_used = models.PositiveIntegerField(default=0)
        notes = models.TextField(blank=True)

Field Validation Logic
--------------------

Package Creation Validation
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def clean(self):
        # Validate session counts
        if self.sessions_remaining > self.total_sessions:
            raise ValidationError({
                'sessions_remaining': _('Remaining sessions cannot exceed total sessions')
            })
            
        # Validate dates
        if self.expiry_date and self.expiry_date < self.purchase_date:
            raise ValidationError({
                'expiry_date': _('Expiry date must be after purchase date')
            })
            
        # Validate pricing
        if self.service and self.per_session_price > self.service.price:
            raise ValidationError({
                'per_session_price': _('Per-session price cannot exceed service price')
            })

        # Corporate package validation
        if self.organization and not self.service.is_corporate_eligible:
            raise ValidationError({
                'service': _('Selected service is not eligible for corporate packages')
            })

Package Usage Validation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def use_session(self, booking):
        """Use a session from this package."""
        if not self.active:
            raise ValidationError(_("Cannot use sessions from an inactive package"))
            
        if self.sessions_remaining <= 0:
            raise ValidationError(_("No sessions remaining in this package"))
            
        if self.expiry_date < timezone.now().date():
            raise ValidationError(_("Package has expired"))
            
        if booking.service != self.service:
            raise ValidationError(_("Booking service does not match package service"))
            
        # Deduct a session
        self.sessions_remaining -= 1
        if self.sessions_remaining == 0:
            self.active = False
            
        self.save()
        
        # Create usage record
        PackageUsage.objects.create(
            package=self,
            booking=booking,
            date_used=timezone.now()
        )

API Endpoints
------------

Package Management
~~~~~~~~~~~~~~~~

**GET** ``/api/packages/``

* Lists packages with filtering options
* Parameters:
  * ``owner`` - Filter by owner ID
  * ``service`` - Filter by service ID
  * ``active`` - Filter by active status
  * ``available`` - Filter packages with remaining sessions
  * ``organization`` - Filter by organization ID

**POST** ``/api/packages/``

* Creates a new package
* Required fields:
  * ``service`` - Service ID
  * ``total_sessions`` - Number of sessions
  * ``price`` - Total package price
  * ``expiry_date`` - Package expiration date
* Validation:
  * Validates service exists
  * Ensures price is valid compared to service price
  * Calculates per-session price

**GET** ``/api/packages/{id}/``

* Returns detailed information about a specific package
* Includes usage history and client assignments

**PUT/PATCH** ``/api/packages/{id}/``

* Updates package information
* Restricted fields:
  * Cannot reduce sessions below used count
  * Cannot change service for packages with usage

**DELETE** ``/api/packages/{id}/``

* Deactivates a package (soft delete)
* Not allowed for packages with usage records

Package Transfers
~~~~~~~~~~~~~~~

**POST** ``/api/packages/{id}/transfer/``

* Transfers a package to another client
* Required fields:
  * ``new_owner`` - User ID of the new owner
* Validation:
  * Package must be transferable
  * Both users must be active
  * Package must have remaining sessions

Package Usage
~~~~~~~~~~~

**GET** ``/api/packages/{id}/usage/``

* Returns usage history for a package
* Includes booking details and timestamps

**POST** ``/api/packages/{id}/use/``

* Records usage of a package session
* Required fields:
  * ``booking_id`` - ID of the booking using this package
* Validation:
  * Package must be active
  * Must have sessions remaining
  * Must not be expired

Integration Points
-----------------

* **Bookings Module**: Validates and tracks package usage during booking
* **Services Module**: Links packages to specific services
* **Users Module**: Manages package ownership and client assignments
* **Organizations Module**: Handles corporate package allocation

Best Practices
-------------

1. **Package Creation**
   * Set appropriate expiration dates based on package size
   * Ensure pricing reflects actual discounts
   * Use clear naming conventions for package identification

2. **Client Communication**
   * Notify clients of package expiration in advance
   * Display remaining sessions prominently in the UI
   * Provide usage history for transparency

3. **Error Handling**
   * Implement graceful handling for expired packages
   * Provide clear messages when session limits are reached
   * Handle edge cases like service discontinuation

4. **Performance Considerations**
   * Index package queries by owner and expiration date
   * Cache package availability status
   * Optimize queries for high-volume package checks

Example Usage
------------

Booking with Package
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Example of package usage in booking creation
    def create_booking_with_package(client, service, date, time, package_id=None):
        # Create the booking
        booking = Booking.objects.create(
            client=client,
            service=service,
            start_time=datetime.combine(date, time)
        )
        
        if package_id:
            try:
                # Get package and validate
                package = Package.objects.get(
                    id=package_id, 
                    owner=client,
                    active=True,
                    service=service
                )
                
                # Use a session from the package
                package.use_session(booking)
                
                # Link booking to package
                BookingPackage.objects.create(
                    booking=booking,
                    package=package,
                    owner=client
                )
                
            except ValidationError as e:
                # Handle validation errors
                booking.delete()
                raise e
                
        return booking
