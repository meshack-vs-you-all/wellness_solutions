Schedules Module
===============

Overview
--------

The Schedules module provides a comprehensive system for managing calendars, availability, and timetables across the entire platform. It handles recurring schedules, exceptions, blocked periods, and integrates with bookings, locations, and instructor availability to ensure reliable scheduling operations.

Core Features
------------

* **Calendar Management**: Central scheduling system for all entities
* **Recurring Patterns**: Support for regular weekly schedules
* **Exception Handling**: Management of holidays, closures, and special hours
* **Resource Conflict Prevention**: Prevent double-booking of instructors or spaces
* **Capacity Management**: Track and enforce maximum occupancy limits
* **Time Zone Support**: Handling of schedules across different time zones
* **Integration**: Seamless connection with bookings, locations, and instructors

Data Models
----------

Schedule Model
~~~~~~~~~~~~

The base model for defining schedules:

.. code-block:: python

    class Schedule(TimeStampedModel):
        """Model for managing schedules and timetables."""
        
        name = models.CharField(max_length=100)
        description = models.TextField(blank=True)
        active = models.BooleanField(default=True)
        
        # Schedule owner (user, location, or organization)
        content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
        object_id = models.PositiveIntegerField()
        content_object = GenericForeignKey('content_type', 'object_id')
        
        # Default time zone
        time_zone = models.CharField(
            max_length=50,
            default='UTC',
            choices=[(tz, tz) for tz in pytz.common_timezones]
        )
        
        class Meta:
            verbose_name = _('Schedule')
            verbose_name_plural = _('Schedules')
            
        def __str__(self):
            return f"{self.name} ({self.content_object})"
            
        def get_recurring_events(self, start_date, end_date):
            """Get all recurring events in this schedule within date range."""
            return self.recurring_events.filter(
                Q(end_date__isnull=True) | Q(end_date__gte=start_date),
                start_date__lte=end_date,
                active=True
            )
            
        def get_exceptions(self, start_date, end_date):
            """Get all exceptions in this schedule within date range."""
            return self.exceptions.filter(
                date__gte=start_date,
                date__lte=end_date
            )
            
        def is_available(self, start_datetime, end_datetime):
            """Check if this schedule is available for the given time period."""
            # Convert to schedule's time zone
            tz = pytz.timezone(self.time_zone)
            start = start_datetime.astimezone(tz)
            end = end_datetime.astimezone(tz)
            
            date = start.date()
            day_name = start.strftime('%A').lower()
            
            # Check for exceptions first
            exception = self.exceptions.filter(date=date).first()
            if exception:
                if not exception.available:
                    return False
                    
                # Check if within exception hours
                if exception.override_hours:
                    within_hours = False
                    for slot in exception.hours:
                        slot_start = datetime.combine(date, slot['start'])
                        slot_end = datetime.combine(date, slot['end'])
                        if slot_start <= start and end <= slot_end:
                            within_hours = True
                            break
                    return within_hours
            
            # Check recurring events
            recurring = self.recurring_events.filter(
                day_of_week=day_name,
                start_date__lte=date,
                Q(end_date__isnull=True) | Q(end_date__gte=date),
                active=True
            )
            
            if not recurring.exists():
                return False
                
            # Check if within recurring hours
            for event in recurring:
                if event.start_time <= start.time() and end.time() <= event.end_time:
                    return True
                    
            return False

RecurringEvent Model
~~~~~~~~~~~~~~~~~~

For defining regular weekly schedules:

.. code-block:: python

    class RecurringEvent(TimeStampedModel):
        """Model for recurring schedule events."""
        
        schedule = models.ForeignKey(
            Schedule,
            on_delete=models.CASCADE,
            related_name='recurring_events'
        )
        
        DAYS_OF_WEEK = [
            ('monday', _('Monday')),
            ('tuesday', _('Tuesday')),
            ('wednesday', _('Wednesday')),
            ('thursday', _('Thursday')),
            ('friday', _('Friday')),
            ('saturday', _('Saturday')),
            ('sunday', _('Sunday')),
        ]
        
        day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
        start_time = models.TimeField()
        end_time = models.TimeField()
        start_date = models.DateField(default=timezone.now)
        end_date = models.DateField(null=True, blank=True)
        active = models.BooleanField(default=True)
        
        # Additional metadata
        title = models.CharField(max_length=100, blank=True)
        notes = models.TextField(blank=True)
        
        class Meta:
            verbose_name = _('Recurring Event')
            verbose_name_plural = _('Recurring Events')
            ordering = ['day_of_week', 'start_time']
            
        def __str__(self):
            return f"{self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
            
        def clean(self):
            super().clean()
            # Validate time range
            if self.start_time >= self.end_time:
                raise ValidationError({
                    'end_time': _('End time must be after start time')
                })
                
            # Validate date range
            if self.end_date and self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': _('End date must be after start date')
                })

ScheduleException Model
~~~~~~~~~~~~~~~~~~~~~

For handling special dates and exceptions:

.. code-block:: python

    class ScheduleException(TimeStampedModel):
        """Model for schedule exceptions like holidays and special hours."""
        
        schedule = models.ForeignKey(
            Schedule,
            on_delete=models.CASCADE,
            related_name='exceptions'
        )
        date = models.DateField()
        title = models.CharField(max_length=100)
        available = models.BooleanField(default=False)
        override_hours = models.BooleanField(
            default=False,
            help_text=_('Override regular hours with custom hours')
        )
        hours = models.JSONField(
            default=list,
            blank=True,
            help_text=_('Custom hours in JSON format')
        )
        notes = models.TextField(blank=True)
        
        class Meta:
            verbose_name = _('Schedule Exception')
            verbose_name_plural = _('Schedule Exceptions')
            ordering = ['date']
            unique_together = ['schedule', 'date']
            
        def __str__(self):
            return f"{self.title} - {self.date}"
            
        def clean(self):
            super().clean()
            # Validate hours if overriding
            if self.override_hours and not self.available:
                raise ValidationError({
                    'override_hours': _('Cannot override hours when not available')
                })
                
            if self.override_hours:
                # Validate hours JSON structure
                if not isinstance(self.hours, list):
                    raise ValidationError({
                        'hours': _('Hours must be a list of time slots')
                    })
                    
                for slot in self.hours:
                    if not isinstance(slot, dict) or 'start' not in slot or 'end' not in slot:
                        raise ValidationError({
                            'hours': _('Invalid time slot format')
                        })
                        
                    # Validate time formats
                    try:
                        start_time = datetime.strptime(slot['start'], '%H:%M').time()
                        end_time = datetime.strptime(slot['end'], '%H:%M').time()
                        
                        if start_time >= end_time:
                            raise ValidationError({
                                'hours': _('End time must be after start time')
                            })
                    except (ValueError, TypeError):
                        raise ValidationError({
                            'hours': _('Invalid time format (use HH:MM)')
                        })

Calendar Generation
------------------

The module provides powerful calendar generation functionality:

.. code-block:: python

    def generate_calendar_events(schedule, start_date, end_date):
        """Generate calendar events for a given schedule within a date range."""
        events = []
        
        # Get all recurring events in this schedule
        recurring_events = schedule.get_recurring_events(start_date, end_date)
        
        # Get all exceptions in this date range
        exceptions = {
            ex.date: ex for ex in schedule.get_exceptions(start_date, end_date)
        }
        
        # Generate events for each day in the range
        current_date = start_date
        while current_date <= end_date:
            # Check if this date has an exception
            if current_date in exceptions:
                exception = exceptions[current_date]
                
                # Skip if location is closed on this date
                if not exception.available:
                    current_date += timedelta(days=1)
                    continue
                    
                # Use exception hours if overriding
                if exception.override_hours:
                    for slot in exception.hours:
                        start_time = datetime.strptime(slot['start'], '%H:%M').time()
                        end_time = datetime.strptime(slot['end'], '%H:%M').time()
                        
                        events.append({
                            'title': exception.title,
                            'start': datetime.combine(current_date, start_time),
                            'end': datetime.combine(current_date, end_time),
                            'notes': exception.notes,
                            'is_exception': True
                        })
                    
                    current_date += timedelta(days=1)
                    continue
            
            # Get day of week
            day_name = current_date.strftime('%A').lower()
            
            # Add regular recurring events for this day
            for event in recurring_events.filter(day_of_week=day_name):
                # Skip if this event hasn't started yet or has ended
                if (event.start_date > current_date or 
                    (event.end_date and event.end_date < current_date)):
                    continue
                    
                events.append({
                    'title': event.title or schedule.name,
                    'start': datetime.combine(current_date, event.start_time),
                    'end': datetime.combine(current_date, event.end_time),
                    'notes': event.notes,
                    'is_exception': False,
                    'recurring_id': event.id
                })
            
            current_date += timedelta(days=1)
            
        return events

API Endpoints
------------

Schedule Management
~~~~~~~~~~~~~~~~~

**GET** ``/api/schedules/``

* Lists schedules with filtering options
* Parameters:
  * ``entity_type`` - Filter by entity type (location, instructor, etc.)
  * ``entity_id`` - Filter by specific entity ID
  * ``active`` - Filter by active status
  * ``search`` - Search by schedule name or description

**POST** ``/api/schedules/``

* Creates a new schedule
* Required fields:
  * ``name`` - Schedule name
  * ``entity_type`` - Entity type (location, instructor, etc.)
  * ``entity_id`` - ID of the entity
* Optional fields:
  * ``description`` - Schedule description
  * ``time_zone`` - Default time zone (default: UTC)

**GET** ``/api/schedules/{id}/``

* Returns detailed information about a specific schedule
* Includes recurring events and exceptions

**PUT/PATCH** ``/api/schedules/{id}/``

* Updates schedule information
* Restricted fields based on user role

Recurring Events
~~~~~~~~~~~~~~

**GET** ``/api/schedules/{id}/events/``

* Lists recurring events for a schedule
* Parameters:
  * ``day`` - Filter by day of week
  * ``active`` - Filter by active status

**POST** ``/api/schedules/{id}/events/``

* Creates a new recurring event
* Required fields:
  * ``day_of_week`` - Day of the week
  * ``start_time`` - Start time
  * ``end_time`` - End time
* Validation:
  * End time must be after start time
  * No overlapping events on the same day

**DELETE** ``/api/schedules/{id}/events/{event_id}/``

* Deletes a recurring event
* Optional parameters:
  * ``deactivate_only`` - If true, marks as inactive instead of deleting

Schedule Exceptions
~~~~~~~~~~~~~~~~~

**GET** ``/api/schedules/{id}/exceptions/``

* Lists exceptions for a schedule
* Parameters:
  * ``start_date`` - Start of date range
  * ``end_date`` - End of date range
  * ``available`` - Filter by availability

**POST** ``/api/schedules/{id}/exceptions/``

* Creates a new schedule exception
* Required fields:
  * ``date`` - Exception date
  * ``title`` - Exception title
  * ``available`` - Whether the entity is available
* Optional fields:
  * ``override_hours`` - Whether to override regular hours
  * ``hours`` - Custom hours if overriding

Calendar Integration
~~~~~~~~~~~~~~~~~~

**GET** ``/api/schedules/{id}/calendar/``

* Returns calendar events for a schedule
* Parameters:
  * ``start_date`` - Start of date range (required)
  * ``end_date`` - End of date range (required)
  * ``format`` - Output format (json, ical)
* Returns:
  * Calendar events within the specified range
  * Merged exceptions and recurring events

Integration Points
-----------------

* **Locations Module**: Operating hours and special closures
* **Instructors Module**: Availability and time off
* **Bookings Module**: Appointment scheduling and conflict prevention
* **Services Module**: Service scheduling constraints

Best Practices
-------------

1. **Schedule Creation**
   * Define clear default schedules for all entities
   * Use consistent naming conventions
   * Set appropriate time zones

2. **Exception Handling**
   * Plan for holidays and special events in advance
   * Clearly document reasons for exceptions
   * Notify affected users of schedule changes

3. **Conflict Prevention**
   * Validate all scheduling changes against existing bookings
   * Implement buffer times between appointments
   * Consider travel time for multi-location schedules

4. **Performance Considerations**
   * Cache frequently accessed schedules
   * Limit calendar generation to reasonable date ranges
   * Optimize database queries for schedule lookups

Example Usage
------------

Checking Availability
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def check_booking_availability(service, location, start_time, end_time):
        """Check if a booking can be made for the given parameters."""
        # Check location schedule
        location_schedule = Schedule.objects.get(
            content_type=ContentType.objects.get_for_model(Location),
            object_id=location.id
        )
        
        if not location_schedule.is_available(start_time, end_time):
            return {
                'available': False,
                'reason': 'Location is not available at this time'
            }
            
        # Check location capacity
        concurrent_bookings = Booking.objects.filter(
            location=location,
            status__in=['confirmed', 'pending'],
            start_time__lt=end_time,
            end_time__gt=start_time
        ).count()
        
        if concurrent_bookings >= location.capacity:
            return {
                'available': False,
                'reason': 'Location is at full capacity'
            }
            
        # Find available instructors
        available_instructors = []
        for instructor in location.get_active_instructors():
            instructor_schedule = Schedule.objects.get(
                content_type=ContentType.objects.get_for_model(WellnessInstructor),
                object_id=instructor.id
            )
            
            if instructor_schedule.is_available(start_time, end_time):
                # Check if instructor has conflicting bookings
                has_conflict = Booking.objects.filter(
                    instructor=instructor,
                    status__in=['confirmed', 'pending'],
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()
                
                if not has_conflict:
                    available_instructors.append(instructor)
        
        if not available_instructors:
            return {
                'available': False,
                'reason': 'No instructors available at this time'
            }
            
        return {
            'available': True,
            'available_instructors': available_instructors
        }
