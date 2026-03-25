Bookings Module
==============

Overview
--------

The Bookings module is a comprehensive system for managing client appointments, scheduling, and calendar management. It handles the entire booking lifecycle from creation to completion, including notifications, reminders, and integration with instructor and location availability.

Core Features
------------

* **Appointment Creation and Management**: Create, modify, and cancel bookings through UI or API
* **Resource Availability Checking**: Real-time validation of instructor and location availability
* **Automatic Reminders**: Email and SMS notifications for upcoming appointments
* **Calendar Integration**: Sync with popular calendar systems (Google, Outlook, Apple)
* **Package Integration**: Track and validate service package usage
* **Rescheduling Workflow**: Streamlined process for changing appointment times
* **Booking History**: Complete audit trail of booking changes and statuses

Data Models
----------

Booking Model
~~~~~~~~~~~~

The primary model for managing appointment data:

.. code-block:: python

    class Booking(TimeStampedModel):
        """Model for managing client bookings."""
        
        # Basic Information
        booking_number = models.CharField(unique=True, max_length=20)
        booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES)
        status = models.CharField(max_length=20, choices=STATUS_CHOICES)
        
        # Time and Location
        start_time = models.DateTimeField()
        end_time = models.DateTimeField()
        location = models.ForeignKey('locations.Location', on_delete=models.PROTECT)
        
        # People
        client = models.ForeignKey('users.User', on_delete=models.CASCADE)
        instructor = models.ForeignKey('wellness_instructors.WellnessInstructor', 
                                     on_delete=models.PROTECT)
        
        # Service Details
        service = models.ForeignKey('services.Service', on_delete=models.PROTECT)
        organization = models.ForeignKey('services.Organization', 
                                       on_delete=models.SET_NULL, null=True, blank=True)
        
        # Payment
        payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
        total_price = models.DecimalField(max_digits=10, decimal_places=2)
        
        # Additional Information
        notes = models.TextField(blank=True)
        cancellation_reason = models.TextField(blank=True)

Key validation rules:
* End time must be after start time
* Start time cannot be in the past for new bookings
* Instructor and location must be available for the requested time slot
* Client must have appropriate permissions for the service

BookingPackage Model
~~~~~~~~~~~~~~~~~~~

Links bookings to service packages:

.. code-block:: python

    class BookingPackage(TimeStampedModel):
        """Model for tracking package usage through bookings."""
        
        booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
        package = models.ForeignKey('packages.Package', on_delete=models.PROTECT)
        sessions_used = models.PositiveIntegerField(default=1)
        owner = models.ForeignKey('users.User', on_delete=models.CASCADE)

API Endpoints
------------

Booking Management
~~~~~~~~~~~~~~~~

**GET** ``/api/bookings/``

* Lists bookings with filtering options
* Parameters:
  * ``client`` - Filter by client ID
  * ``instructor`` - Filter by instructor ID
  * ``status`` - Filter by booking status
  * ``start_after`` - Filter by start time after date
  * ``start_before`` - Filter by start time before date
  * ``location`` - Filter by location ID

**POST** ``/api/bookings/``

* Creates a new booking
* Required fields:
  * ``service`` - Service ID
  * ``start_time`` - Appointment start time
  * ``location`` - Location ID
  * ``instructor`` - Instructor ID (optional if auto-assignment enabled)
* Validation:
  * Checks instructor availability
  * Validates location operating hours
  * Ensures client package has sufficient sessions if package is specified

**GET** ``/api/bookings/{id}/``

* Returns detailed information about a specific booking
* Includes client details, payment status, and booking history

**PUT/PATCH** ``/api/bookings/{id}/``

* Updates booking information
* Status transitions follow business rules
* Triggers notifications for relevant changes

**DELETE** ``/api/bookings/{id}/``

* Cancels a booking (soft delete)
* Requires cancellation reason
* May trigger refund process based on cancellation policy

Availability Checking
~~~~~~~~~~~~~~~~~~~

**GET** ``/api/bookings/availability/``

* Checks resource availability for potential bookings
* Parameters:
  * ``start_time`` - Desired start time
  * ``end_time`` - Desired end time
  * ``service_id`` - Service to book
  * ``location_id`` - Optional location filter
  * ``instructor_id`` - Optional instructor filter
* Returns:
  * Available time slots
  * Available instructors
  * Available locations

Calendar Integration
~~~~~~~~~~~~~~~~~~

**GET** ``/api/bookings/calendar/{user_id}/``

* Returns calendar data for a user (client or instructor)
* Parameters:
  * ``start_date`` - Calendar start date
  * ``end_date`` - Calendar end date
  * ``include_details`` - Boolean to include booking details
* Supports iCal, Google Calendar, and other formats

Best Practices
-------------

1. **Availability Checking**
   * Always check instructor and location availability before creating a booking
   * Use the availability endpoint to validate time slots
   * Consider time zone differences when booking

2. **Error Handling**
   * Handle booking conflicts gracefully
   * Provide clear error messages with suggested alternatives
   * Implement retry mechanisms for temporary availability issues

3. **Notifications**
   * Send confirmation emails/SMS for all booking actions
   * Include calendar attachments (.ics files)
   * Send reminders 24 hours before appointment

4. **Cancellation Policies**
   * Clearly communicate cancellation deadlines
   * Apply appropriate refund policies
   * Track cancellation reasons for reporting

5. **Performance Considerations**
   * Use database indexing for booking queries
   * Implement caching for availability checks
   * Optimize calendar queries for date ranges

Integration Points
-----------------

* **User Module**: Authentication and client information
* **Locations Module**: Facility data and operating hours
* **Services Module**: Service details and pricing
* **Packages Module**: Package validation and usage tracking
* **Instructors Module**: Instructor profiles and availability
* **Notifications System**: Email and SMS alerts
* **Payment Gateway**: Payment processing for bookings
