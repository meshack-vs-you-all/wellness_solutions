Wellness Instructors Module
=======================

Overview
--------

The Wellness Instructors module manages all aspects of instructor profiles, qualifications, scheduling, and availability. It provides a comprehensive system for instructor management, assignment to locations, service specializations, and integration with the booking system.

Core Features
------------

* **Instructor Profiles**: Detailed profiles with qualifications and specialties
* **Availability Management**: Flexible scheduling rules and calendar integration
* **Location Assignments**: Assignment of instructors to multiple locations
* **Performance Tracking**: Client feedback and session metrics
* **Service Specializations**: Linking instructors to specific services
* **Workload Balancing**: Equitable distribution of sessions
* **Certification Management**: Tracking and renewal of instructor certifications

Data Models
----------

WellnessInstructor Model
~~~~~~~~~~~~~~~~~~~~~

The primary model for instructor information:

.. code-block:: python

    class WellnessInstructor(TimeStampedModel):
        """Model for managing wellness instructors."""
        
        # Personal Information
        user = models.OneToOneField(
            'users.User',
            on_delete=models.CASCADE,
            related_name='instructor_profile'
        )
        bio = models.TextField(blank=True)
        profile_image = models.ImageField(upload_to='instructors/', blank=True)
        
        # Qualifications
        qualifications = models.TextField(blank=True)
        certification_level = models.CharField(
            max_length=20,
            choices=CERTIFICATION_LEVELS,
            default='level1'
        )
        years_experience = models.PositiveIntegerField(default=0)
        
        # Specializations
        specialties = models.ManyToManyField(
            'services.Service',
            related_name='specialized_instructors',
            blank=True
        )
        
        # Operational Status
        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='active'
        )
        
        # Availability
        default_availability = models.JSONField(default=dict, validators=[validate_availability])
        max_sessions_per_day = models.PositiveIntegerField(default=8)
        
        # Compensation
        hourly_rate = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            validators=[MinValueValidator(0)]
        )
        
        # Tracking Metrics
        total_sessions = models.PositiveIntegerField(default=0)
        average_rating = models.DecimalField(
            max_digits=3,
            decimal_places=2,
            default=Decimal('0.00'),
            validators=[MinValueValidator(0), MaxValueValidator(5)]
        )

Key validation rules:
* Certification level must be valid
* Default availability must follow the standard availability format
* Maximum sessions per day must be reasonable (1-16)
* Hourly rate must be positive

InstructorCertification Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tracks instructor certifications:

.. code-block:: python

    class InstructorCertification(TimeStampedModel):
        """Model for tracking instructor certifications."""
        
        instructor = models.ForeignKey(
            WellnessInstructor,
            on_delete=models.CASCADE,
            related_name='certifications'
        )
        name = models.CharField(max_length=100)
        issuing_organization = models.CharField(max_length=100)
        date_issued = models.DateField()
        expiration_date = models.DateField(null=True, blank=True)
        certification_id = models.CharField(max_length=100, blank=True)
        verification_url = models.URLField(blank=True)
        active = models.BooleanField(default=True)
        
        class Meta:
            ordering = ['-date_issued']
            
        def __str__(self):
            return f"{self.name} - {self.instructor.user.get_full_name()}"
            
        def clean(self):
            super().clean()
            # Validate dates
            if self.expiration_date and self.expiration_date < self.date_issued:
                raise ValidationError({
                    'expiration_date': _('Expiration date cannot be before date issued')
                })
                
            # Update active status based on expiration
            if self.expiration_date and self.expiration_date < timezone.now().date():
                self.active = False

Field Validation Logic
--------------------

Availability Validation
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def validate_availability(value):
        """Validate the availability JSON structure."""
        if not isinstance(value, dict):
            raise ValidationError(_('Availability must be a dictionary'))
            
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        
        # Check that all days are included
        for day in days_of_week:
            if day not in value:
                raise ValidationError(_(f'Missing day in availability: {day}'))
                
        # Validate time slots for each day
        for day, slots in value.items():
            if day not in days_of_week:
                raise ValidationError(_(f'Invalid day: {day}'))
                
            if not isinstance(slots, list):
                raise ValidationError(_(f'Time slots for {day} must be a list'))
                
            # Validate each time slot
            for slot in slots:
                if not isinstance(slot, dict) or 'start' not in slot or 'end' not in slot:
                    raise ValidationError(_(f'Invalid time slot format for {day}'))
                    
                # Validate time format (HH:MM)
                for key in ['start', 'end']:
                    time_str = slot[key]
                    try:
                        hour, minute = map(int, time_str.split(':'))
                        if not (0 <= hour <= 23 and 0 <= minute <= 59):
                            raise ValueError
                    except (ValueError, TypeError):
                        raise ValidationError(_(f'Invalid time format for {day}: {time_str}'))
                        
                # Validate that end time is after start time
                start_parts = list(map(int, slot['start'].split(':')))
                end_parts = list(map(int, slot['end'].split(':')))
                
                start_minutes = start_parts[0] * 60 + start_parts[1]
                end_minutes = end_parts[0] * 60 + end_parts[1]
                
                if end_minutes <= start_minutes:
                    raise ValidationError(_(f'End time must be after start time for {day}'))

Instructor Availability Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def is_available(self, start_time, end_time, location=None):
        """
        Check if instructor is available for a given time slot at a specific location.
        
        Args:
            start_time (datetime): Start time of the booking
            end_time (datetime): End time of the booking
            location (Location, optional): Specific location to check
            
        Returns:
            bool: True if available, False otherwise
        """
        # Check instructor status
        if self.status != 'active':
            return False
            
        # Check if date is blocked in special dates
        date = start_time.date()
        if SpecialDate.objects.filter(
            instructor=self,
            date=date,
            is_available=False
        ).exists():
            return False
            
        # Check default availability for day of week
        day_of_week = start_time.strftime('%A').lower()
        default_avail = self.default_availability.get(day_of_week, [])
        
        # Convert times to minutes for easier comparison
        start_minutes = start_time.hour * 60 + start_time.minute
        end_minutes = end_time.hour * 60 + end_time.minute
        
        # Check if time slot falls within any available slots
        is_within_default = False
        for slot in default_avail:
            slot_start = list(map(int, slot['start'].split(':')))
            slot_end = list(map(int, slot['end'].split(':')))
            
            slot_start_minutes = slot_start[0] * 60 + slot_start[1]
            slot_end_minutes = slot_end[0] * 60 + slot_end[1]
            
            if (slot_start_minutes <= start_minutes and 
                end_minutes <= slot_end_minutes):
                is_within_default = True
                break
                
        if not is_within_default:
            return False
            
        # Check if instructor is assigned to this location
        if location and not LocationInstructor.objects.filter(
            instructor=self,
            location=location,
            status='active'
        ).exists():
            return False
            
        # Check for conflicting bookings
        conflicting_bookings = Booking.objects.filter(
            instructor=self,
            status__in=['confirmed', 'pending'],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()
        
        if conflicting_bookings:
            return False
            
        # Check max sessions per day
        sessions_today = Booking.objects.filter(
            instructor=self,
            status__in=['confirmed', 'pending'],
            start_time__date=date
        ).count()
        
        if sessions_today >= self.max_sessions_per_day:
            return False
            
        return True

API Endpoints
------------

Instructor Management
~~~~~~~~~~~~~~~~~~~

**GET** ``/api/instructors/``

* Lists all instructors with filtering options
* Parameters:
  * ``status`` - Filter by instructor status
  * ``location_id`` - Filter by assigned location
  * ``service_id`` - Filter by service specialization
  * ``certification`` - Filter by certification type
  * ``search`` - Search by name, qualifications, or specialties

**POST** ``/api/instructors/``

* Creates a new instructor profile
* Required fields:
  * ``user_id`` - User ID to associate with instructor profile
  * ``certification_level`` - Instructor's certification level
  * ``hourly_rate`` - Base compensation rate
* Validation:
  * User must not already have an instructor profile
  * Certification level must be valid
  * Hourly rate must be positive

**GET** ``/api/instructors/{id}/``

* Returns detailed information about a specific instructor
* Includes specializations, certifications, and location assignments

**PUT/PATCH** ``/api/instructors/{id}/``

* Updates instructor information
* Restricted fields based on user role
* Validates certification changes

Instructor Availability
~~~~~~~~~~~~~~~~~~~~~

**GET** ``/api/instructors/{id}/availability/``

* Returns instructor's availability calendar
* Parameters:
  * ``start_date`` - Start of date range (required)
  * ``end_date`` - End of date range (required)
  * ``location_id`` - Filter by location
* Returns:
  * Available time slots for each day
  * Booked sessions (anonymized)
  * Blocked dates and times

**POST** ``/api/instructors/{id}/availability/``

* Updates instructor's availability
* Required fields:
  * ``availability`` - JSON object with day-by-day availability
* Validation:
  * Validates time slot formats
  * Ensures no conflicts with existing bookings

**POST** ``/api/instructors/{id}/block-dates/``

* Blocks specific dates or time ranges
* Required fields:
  * ``start_date`` - Start date to block
  * ``end_date`` - End date to block (can be same as start_date)
  * ``all_day`` - Boolean indicating if entire day is blocked
  * ``start_time`` - Start time if not all day
  * ``end_time`` - End time if not all day
* Validation:
  * Cannot block dates with existing bookings

Instructor Locations
~~~~~~~~~~~~~~~~~~

**GET** ``/api/instructors/{id}/locations/``

* Lists locations assigned to an instructor
* Includes assignment status and scheduling preferences

**POST** ``/api/instructors/{id}/locations/``

* Assigns instructor to a location
* Required fields:
  * ``location_id`` - Location to assign
  * ``status`` - Assignment status (active, inactive, temporary)
* Optional fields:
  * ``is_primary`` - Whether this is instructor's primary location
  * ``availability_rules`` - Location-specific availability rules

Integration Points
-----------------

* **Users Module**: Instructor accounts and authentication
* **Locations Module**: Facility assignments and location-specific availability
* **Bookings Module**: Session scheduling and conflict detection
* **Services Module**: Service specializations and eligibility

Best Practices
-------------

1. **Instructor Assignment**
   * Match client preferences with instructor specialties
   * Consider travel time between locations for multi-location instructors
   * Balance workload across the instructor team

2. **Availability Management**
   * Use clear default availability templates
   * Allow for special date exceptions
   * Implement buffer times between sessions

3. **Performance Monitoring**
   * Track client feedback consistently
   * Monitor session completion rates
   * Review certification currency regularly

4. **Scheduling Optimization**
   * Group sessions by location to minimize travel
   * Consider instructor preferences for time of day
   * Allocate appropriate preparation time

Dashboard Features
---------------

The instructor dashboard provides a centralized interface for instructors to manage their schedule:

* **Today's Schedule**: Quick view of upcoming sessions
* **Availability Management**: Calendar interface for setting availability
* **Client Information**: Access to relevant client details and preferences
* **Performance Metrics**: Session counts, ratings, and feedback
* **Certification Tracking**: Status of current certifications and renewal reminders
