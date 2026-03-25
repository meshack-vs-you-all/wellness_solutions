Locations Management System
======================

The Locations module provides a comprehensive management system for physical and virtual locations where services are provided. This module is tightly integrated with the scheduling and instructor management systems to enable efficient resource allocation and service delivery.

Architecture Overview
-------------------

The Locations module follows a layered architecture:

1. **Models Layer**: Core data models representing locations, services, and assignments
2. **Business Logic Layer**: Service classes implementing business rules and validations
3. **API Layer**: RESTful endpoints for location management
4. **Permission Layer**: Role-based access controls for location operations

Core Models
----------

Location
~~~~~~~

The ``Location`` model represents physical and virtual locations where services can be provided.

Fields
~~~~~~

- ``name`` (CharField): Location name (max length: 100, unique)
- ``type`` (CharField): Type of location. Options:
    - ``studio``: Physical studio location
    - ``virtual``: Virtual/online location
    - ``onsite``: On-site location at client premises
    - ``hybrid``: Combination of physical and virtual services
- ``address`` (TextField): Physical address (optional for virtual locations)
- ``coordinates`` (PointField): Geographical coordinates for mapping
- ``contact_info`` (JSONField): Contact information in JSON format containing:
    - ``phone``: Contact phone number (must start with '+' and contain at least 10 characters)
    - ``email``: Valid email address with format validation
    - ``website``: Optional website URL
    - ``contact_person``: Primary contact person's name
- ``operating_hours`` (JSONField): Operating hours for each day of the week in format:

.. code-block:: json

    {
        "monday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
        "tuesday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
        "wednesday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
        "thursday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
        "friday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
        "saturday": {"open": "10:00", "close": "15:00", "breaks": []},
        "sunday": {"open": "10:00", "close": "15:00", "breaks": []}
    }

- ``capacity`` (PositiveIntegerField): Maximum capacity of the location
- ``resources`` (JSONField): Available resources at the location (equipment, rooms, etc.)
- ``amenities`` (ArrayField): List of amenities available at the location
- ``status`` (CharField): Current status. Options:
    - ``active``: Location is fully operational
    - ``inactive``: Location is not operational
    - ``maintenance``: Location is under maintenance
    - ``limited``: Location is operating with limited capacity
- ``organization`` (ForeignKey): Associated organization (optional)
- ``metadata`` (JSONField): Additional configurable metadata
- ``created_at`` (DateTimeField): Creation timestamp
- ``updated_at`` (DateTimeField): Last update timestamp

Validation Rules
~~~~~~~~~~~~~~

The model implements comprehensive validation rules:

1. Capacity must be a positive integer
2. Contact information must include valid phone (starts with '+', 10+ chars) and email
3. Operating hours must be specified for all days of the week
4. Location names must be unique across the system
5. Location type must be one of: studio, virtual, onsite, or hybrid
6. Status must be one of: active, inactive, maintenance, or limited
7. Coordinates must be valid geographical points
8. Address is required for non-virtual locations
9. Operating hours must follow valid time formats (HH:MM)
10. Resources and amenities must follow predefined schemas

Business Methods
~~~~~~~~~~~~~~

- ``is_available(date, time_slot)``: Checks availability at specified date/time
- ``calculate_utilization(start_date, end_date)``: Calculates utilization percentage
- ``get_available_instructors(date, time_slot)``: Returns available instructors
- ``get_booking_conflicts(date, time_slot)``: Detects scheduling conflicts
- ``get_capacity_stats()``: Returns capacity statistics and peak times
- ``get_operating_status()``: Returns current operating status with reason

Location Service
~~~~~~~~~~~~~~

The ``LocationService`` model manages services offered at specific locations with dynamic pricing and availability rules.

Fields
~~~~~~

- ``location`` (ForeignKey): Reference to the Location
- ``service`` (ForeignKey): Reference to the Service
- ``price_adjustment`` (DecimalField): Price adjustment for this service at this location
- ``custom_duration`` (PositiveIntegerField): Custom duration for this service at this location (in minutes)
- ``availability_rules`` (JSONField): Rules for service availability including:
    - ``days``: Days of week when available
    - ``time_slots``: Time slots when available
    - ``blackout_dates``: Dates when service is unavailable
    - ``capacity_override``: Service-specific capacity override
- ``is_available`` (BooleanField): Whether this service is currently available
- ``requires_equipment`` (BooleanField): Whether this service requires special equipment
- ``required_certifications`` (ArrayField): Required instructor certifications
- ``notes`` (TextField): Additional notes about the service at this location
- ``created_at`` (DateTimeField): Creation timestamp
- ``updated_at`` (DateTimeField): Last update timestamp

Validation Rules
~~~~~~~~~~~~~~

1. Location and service combination must be unique
2. Free services cannot have price adjustments
3. Location must be active to offer services
4. Availability rules must follow the specified JSON schema
5. Custom duration must be a positive integer
6. Required certifications must exist in the system
7. Price adjustment must be within reasonable limits

Location Instructor
~~~~~~~~~~~~~~~~

The ``LocationInstructor`` model manages instructor assignments to locations with advanced scheduling capabilities.

Fields
~~~~~~

- ``location`` (ForeignKey): Reference to the Location
- ``instructor`` (ForeignKey): Reference to the WellnessInstructor
- ``availability_rules`` (JSONField): Instructor availability rules including:
    - ``recurring``: Weekly recurring availability pattern
    - ``exceptions``: Date-specific exceptions to normal schedule
    - ``vacation_dates``: Planned vacation periods
    - ``preferences``: Time slot preferences (early, mid-day, evening)
- ``is_primary`` (BooleanField): Whether this is the primary location for the instructor
- ``max_sessions_per_day`` (PositiveSmallIntegerField): Maximum sessions per day for this instructor
- ``specializations`` (ArrayField): Specialized services offered by this instructor
- ``status`` (CharField): Status of the instructor at this location. Options:
    - ``active``: Currently active
    - ``inactive``: Not currently active
    - ``temporary``: Temporary assignment
    - ``on_leave``: Temporarily on leave
- ``notes`` (TextField): Additional notes about the instructor at this location
- ``start_date`` (DateField): Assignment start date
- ``end_date`` (DateField): Assignment end date (null if indefinite)
- ``created_at`` (DateTimeField): Creation timestamp
- ``updated_at`` (DateTimeField): Last update timestamp

Validation Rules
~~~~~~~~~~~~~~

1. Location and instructor combination must be unique
2. An instructor can have only one primary location
3. Status must be one of: active, inactive, temporary, or on_leave
4. Availability rules must follow the specified JSON schema
5. End date must be after start date if specified
6. Max sessions per day must be reasonable (1-12)
7. Specializations must match services offered at the location
8. Start date cannot be in the past for new assignments

API Endpoints
-----------

The Locations module provides comprehensive RESTful API endpoints:

Location Management
~~~~~~~~~~~~~~~~

- ``GET /api/locations/`` - List all locations with filtering options
- ``POST /api/locations/`` - Create a new location
- ``GET /api/locations/{id}/`` - Retrieve location details
- ``PUT/PATCH /api/locations/{id}/`` - Update location details
- ``DELETE /api/locations/{id}/`` - Deactivate a location

Location Services
~~~~~~~~~~~~~~~

- ``GET /api/locations/{id}/services/`` - List services at a location
- ``POST /api/locations/{id}/services/`` - Add a service to a location
- ``GET /api/locations/{id}/services/{service_id}/`` - Get service details
- ``PUT/PATCH /api/locations/{id}/services/{service_id}/`` - Update service details
- ``DELETE /api/locations/{id}/services/{service_id}/`` - Remove a service

Location Instructors
~~~~~~~~~~~~~~~~~

- ``GET /api/locations/{id}/instructors/`` - List instructors at a location
- ``POST /api/locations/{id}/instructors/`` - Assign an instructor to a location
- ``GET /api/locations/{id}/instructors/{instructor_id}/`` - Get instructor details
- ``PUT/PATCH /api/locations/{id}/instructors/{instructor_id}/`` - Update instructor assignment
- ``DELETE /api/locations/{id}/instructors/{instructor_id}/`` - Remove instructor assignment

Location Analytics
~~~~~~~~~~~~~~~

- ``GET /api/locations/{id}/analytics/`` - Get location usage analytics
- ``GET /api/locations/{id}/availability/`` - Check availability for specific dates
- ``GET /api/locations/{id}/utilization/`` - Get utilization statistics
- ``GET /api/locations/map/`` - Get all locations with geographical data

Permission Model
--------------

The Locations module implements a comprehensive permission model:

1. **Admin**: Full access to all location operations
2. **Manager**: Create, update, and manage locations and their services
3. **Instructor**: View assigned locations and declare availability
4. **Client**: View location details for booking purposes

Usage Examples
------------

Create a New Location
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wellness_solutions.locations.models import Location

    location = Location.objects.create(
        name="Downtown Studio",
        type="studio",
        address="123 Main St, City, State 12345",
        coordinates=Point(-73.935242, 40.730610),  # longitude, latitude
        contact_info={
            "phone": "+1-123-456-7890",
            "email": "downtown@example.com",
            "website": "https://downtown.example.com",
            "contact_person": "Jane Smith"
        },
        operating_hours={
            "monday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
            "tuesday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
            "wednesday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
            "thursday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
            "friday": {"open": "09:00", "close": "17:00", "breaks": [{"start": "12:00", "end": "13:00"}]},
            "saturday": {"open": "10:00", "close": "15:00", "breaks": []},
            "sunday": {"open": "10:00", "close": "15:00", "breaks": []}
        },
        capacity=50,
        resources={
            "rooms": ["Main Studio", "Private Room 1", "Private Room 2"],
            "equipment": ["Mats", "Bands", "Rollers"]
        },
        amenities=["Showers", "Lockers", "Wifi", "Water Station"],
        status="active"
    )

Check Location Availability
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wellness_solutions.locations.models import Location
    from datetime import datetime, time

    location = Location.objects.get(name="Downtown Studio")
    date = datetime.now().date()
    time_slot = (time(10, 0), time(11, 0))  # 10:00 AM to 11:00 AM

    is_available = location.is_available(date, time_slot)
    if is_available:
        print("Location is available at the specified time")
    else:
        print("Location is not available at the specified time")

Find Available Instructors
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wellness_solutions.locations.models import Location
    from datetime import datetime, time

    location = Location.objects.get(name="Downtown Studio")
    date = datetime.now().date()
    time_slot = (time(14, 0), time(15, 0))  # 2:00 PM to 3:00 PM

    available_instructors = location.get_available_instructors(date, time_slot)
    print(f"Found {len(available_instructors)} available instructors")

Integration Points
---------------

The Locations module integrates with:

1. **Scheduling System**: For room allocation and availability management
2. **Instructor Management**: For instructor assignment and scheduling
3. **Booking System**: For client appointment management
4. **Analytics**: For utilization and performance metrics
5. **Mobile App**: For location search and availability checking
6. **External Calendars**: For calendar syncronization (iCal)
