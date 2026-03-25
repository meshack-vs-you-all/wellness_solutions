API Guidelines
=============

This document outlines the standards and best practices for API development in the Wellness Solutions project.

RESTful API Design Principles
---------------------------

Our APIs follow RESTful design principles:

1. **Resource-Based URLs**: APIs are structured around resources
2. **HTTP Methods**: Use appropriate HTTP methods for operations
   * GET for retrieving data
   * POST for creating resources
   * PUT/PATCH for updating resources
   * DELETE for removing resources
3. **HTTP Status Codes**: Use meaningful status codes
   * 2xx for successful operations
   * 4xx for client errors
   * 5xx for server errors
4. **Consistent Response Format**: Standard structure for all responses
5. **Filtering, Sorting, and Pagination**: Consistent parameters across endpoints
6. **Versioning**: API versioning through URL path (/api/v1/)

URL Structure
-----------

Follow these guidelines for URL structure:

* Use nouns, not verbs (e.g., `/api/v1/bookings/` not `/api/v1/get-bookings/`)
* Use plural resource names (e.g., `/api/v1/users/` not `/api/v1/user/`)
* Use hierarchical structure for related resources (e.g., `/api/v1/organizations/{org_id}/locations/`)
* Use kebab-case for multi-word resource names (e.g., `/api/v1/stretch-instructors/`)
* Include resource ID in URL for specific resource operations (e.g., `/api/v1/bookings/{id}/`)

HTTP Methods
----------

Use HTTP methods appropriately:

* **GET**: Retrieve one or more resources
  * Collection: `/api/v1/bookings/` - Returns a list of bookings
  * Resource: `/api/v1/bookings/{id}/` - Returns a specific booking
  * No side effects

* **POST**: Create a new resource
  * Collection: `/api/v1/bookings/` - Creates a new booking
  * Returns 201 Created with the created resource

* **PUT**: Replace a resource completely
  * Resource: `/api/v1/bookings/{id}/` - Replaces the booking
  * Requires all fields to be provided

* **PATCH**: Update a resource partially
  * Resource: `/api/v1/bookings/{id}/` - Updates specific fields of the booking
  * Only requires the fields being updated

* **DELETE**: Remove a resource
  * Resource: `/api/v1/bookings/{id}/` - Deletes the booking
  * Returns 204 No Content on success

Request/Response Format
---------------------

Standard JSON format for all API requests and responses:

Request Example:

.. code-block:: json

    {
        "client": 123,
        "service": 456,
        "location": 789,
        "instructor": 101,
        "start_time": "2025-05-15T14:00:00Z",
        "end_time": "2025-05-15T15:00:00Z",
        "notes": "First-time client, needs extra care"
    }

Response Example:

.. code-block:: json

    {
        "id": 12345,
        "client": {
            "id": 123,
            "name": "John Smith"
        },
        "service": {
            "id": 456,
            "name": "Deep Tissue Stretch"
        },
        "location": {
            "id": 789,
            "name": "Downtown Studio"
        },
        "instructor": {
            "id": 101,
            "name": "Jane Doe"
        },
        "start_time": "2025-05-15T14:00:00Z",
        "end_time": "2025-05-15T15:00:00Z",
        "status": "confirmed",
        "notes": "First-time client, needs extra care",
        "created": "2025-03-15T10:30:45Z",
        "modified": "2025-03-15T10:30:45Z"
    }

Error Response Example:

.. code-block:: json

    {
        "status": "error",
        "code": "validation_error",
        "message": "Invalid data provided",
        "details": {
            "start_time": ["Start time must be in the future"],
            "instructor": ["Selected instructor is not available at this time"]
        }
    }

HTTP Status Codes
---------------

Use appropriate HTTP status codes:

* **200 OK**: Successful GET, PUT, PATCH, or DELETE
* **201 Created**: Successful resource creation
* **204 No Content**: Successful operation with no response body
* **400 Bad Request**: Invalid request format or validation errors
* **401 Unauthorized**: Missing or invalid authentication
* **403 Forbidden**: Authentication succeeded but insufficient permissions
* **404 Not Found**: Resource not found
* **409 Conflict**: Request conflicts with current state
* **422 Unprocessable Entity**: Validation errors
* **429 Too Many Requests**: Rate limit exceeded
* **500 Internal Server Error**: Server-side error

Filtering, Sorting, and Pagination
--------------------------------

Implement consistent query parameters:

**Filtering**:
* Use field name as parameter: `/api/v1/bookings/?status=confirmed`
* Multiple values: `/api/v1/bookings/?status=confirmed,pending`
* Date ranges: `/api/v1/bookings/?start_date_after=2025-01-01&start_date_before=2025-12-31`
* Search: `/api/v1/bookings/?search=Smith`

**Sorting**:
* Use `ordering` parameter: `/api/v1/bookings/?ordering=start_time`
* Descending order: `/api/v1/bookings/?ordering=-start_time`
* Multiple fields: `/api/v1/bookings/?ordering=-start_time,client__name`

**Pagination**:
* Use `page` and `page_size` parameters: `/api/v1/bookings/?page=2&page_size=25`
* Default page size of 20 items
* Maximum page size of 100 items

Pagination Response Example:

.. code-block:: json

    {
        "count": 243,
        "next": "/api/v1/bookings/?page=3&page_size=20",
        "previous": "/api/v1/bookings/?page=1&page_size=20",
        "results": [
            {
                "id": 12345,
                "client": {
                    "id": 123,
                    "name": "John Smith"
                },
                // ... other booking fields
            },
            // ... more bookings
        ]
    }

Authentication and Authorization
-----------------------------

**Authentication**:
* Use JWT (JSON Web Tokens) for authentication
* Include token in Authorization header: `Authorization: Bearer <token>`
* Refresh tokens for extended sessions

**Authorization**:
* Role-based access control
* Object-level permissions where appropriate
* Permission checks in view classes or permission classes

Field Validation Requirements
--------------------------

Following our Code Quality Rules, all API endpoints must implement comprehensive field validation:

1. **Required Fields**: Check that all required fields are present
2. **Data Types**: Validate correct data types (string, integer, date, etc.)
3. **Value Constraints**: Check minimum/maximum values, length limits, pattern matching
4. **Foreign Key Relationships**: Verify that related objects exist and are valid
5. **Business Rules**: Implement domain-specific validation rules

Example Validation Implementation:

.. code-block:: python

    class BookingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Booking
            fields = ['client', 'service', 'location', 'instructor', 
                      'start_time', 'end_time', 'notes']
        
        def validate(self, data):
            """Validate the entire booking data."""
            # Check that end_time is after start_time
            if data['end_time'] <= data['start_time']:
                raise serializers.ValidationError({
                    'end_time': 'End time must be after start time'
                })
            
            # Check that start_time is in the future
            if data['start_time'] <= timezone.now():
                raise serializers.ValidationError({
                    'start_time': 'Booking must be for a future time'
                })
            
            # Check instructor availability
            instructor = data['instructor']
            if not instructor.is_available(data['start_time'], data['end_time']):
                raise serializers.ValidationError({
                    'instructor': 'Instructor is not available during this time'
                })
            
            # Check location operating hours
            location = data['location']
            if not location.is_open(data['start_time'], data['end_time']):
                raise serializers.ValidationError({
                    'location': 'Location is not open during this time'
                })
            
            return data

Error Handling
------------

Implement consistent error handling across all endpoints:

1. **Descriptive Error Messages**: Clear explanation of what went wrong
2. **Field-Specific Errors**: Associate errors with specific fields where appropriate
3. **Error Codes**: Consistent error codes for common scenarios
4. **Appropriate Status Codes**: Use the correct HTTP status code

Implementation Example:

.. code-block:: python

    try:
        # Database operation
        booking.save()
    except IntegrityError as e:
        # Log the error with context
        logger.error(f"Database integrity error when saving booking: {str(e)}")
        
        # Return appropriate error response
        return Response(
            {
                "status": "error",
                "code": "database_error",
                "message": "Could not create booking due to database constraints",
                "details": str(e)
            },
            status=status.HTTP_409_CONFLICT
        )
    except Exception as e:
        # Log unexpected errors
        logger.exception(f"Unexpected error in booking creation: {str(e)}")
        
        # Return generic error without exposing implementation details
        return Response(
            {
                "status": "error",
                "code": "server_error",
                "message": "An unexpected error occurred"
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

Documentation Requirements
------------------------

All API endpoints must be documented:

1. **Endpoint Description**: What the endpoint does
2. **URL and HTTP Method**: How to access the endpoint
3. **Request Parameters**: Required and optional parameters
4. **Request Body**: Format and fields for POST/PUT/PATCH
5. **Response Format**: Example response with field descriptions
6. **Status Codes**: Possible response status codes
7. **Error Scenarios**: Common error cases

Versioning Strategy
----------------

API versioning allows for backward compatibility:

* **URL Path Versioning**: `/api/v1/`, `/api/v2/`
* **Major Version Changes**: Breaking changes that are not backward compatible
* **Version Lifecycle**:
  * Development: Active development of new features
  * Stable: Maintained with bug fixes and minor enhancements
  * Deprecated: Still available but scheduled for removal
  * Retired: No longer available

Performance Considerations
------------------------

Optimize API performance:

1. **Database Query Optimization**:
   * Use `select_related` and `prefetch_related` for related objects
   * Avoid N+1 query problems
   * Add database indexes for frequently queried fields

2. **Response Size Management**:
   * Use pagination for large collections
   * Allow clients to request specific fields with `fields` parameter
   * Implement nested serialization depth control

3. **Caching Strategy**:
   * Use HTTP caching headers (ETag, Cache-Control)
   * Implement Redis caching for frequent requests
   * Consider cache invalidation strategies

4. **Rate Limiting**:
   * Implement per-user and per-IP rate limits
   * Include rate limit headers in responses
   * Graceful handling of rate limit exceeding

Security Requirements
------------------

Implement these security measures:

1. **Input Validation**: Validate and sanitize all input data
2. **Authentication**: Require authentication for sensitive operations
3. **Authorization**: Check permissions for each request
4. **HTTPS**: Enforce HTTPS for all API communications
5. **CSRF Protection**: Implement for session-based authentication
6. **SQL Injection Prevention**: Use parameterized queries and ORM
7. **Rate Limiting**: Prevent abuse and DoS attacks
8. **Sensitive Data Handling**: Mask sensitive data in logs and responses

API Testing Requirements
---------------------

Every API endpoint must have comprehensive tests:

1. **Unit Tests**: Test serializers and validation logic
2. **Integration Tests**: Test the entire request/response cycle
3. **Authentication Tests**: Verify authentication requirements
4. **Permission Tests**: Check that permission controls work
5. **Edge Case Tests**: Test with boundary values and invalid inputs
6. **Performance Tests**: Verify response times under load

Continuous Integration:
* All tests must pass before merging
* Maintain high code coverage
* Automated API tests run on every pull request

Sample API Test:

.. code-block:: python

    def test_create_booking_validation(self):
        """Test validation rules when creating a booking."""
        url = reverse('booking-list')
        
        # Test with missing required field
        data = {
            'client': self.client.id,
            # Missing service
            'location': self.location.id,
            'instructor': self.instructor.id,
            'start_time': '2025-05-15T14:00:00Z',
            'end_time': '2025-05-15T15:00:00Z'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['code'], 'validation_error')
        self.assertIn('service', response.data['details'])
        
        # Test with invalid time range
        data = {
            'client': self.client.id,
            'service': self.service.id,
            'location': self.location.id,
            'instructor': self.instructor.id,
            'start_time': '2025-05-15T15:00:00Z',  # Start after end
            'end_time': '2025-05-15T14:00:00Z'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('end_time', response.data['details'])

API Changelog
-----------

For any API changes, document in the changelog:

1. **Added**: New endpoints or features
2. **Changed**: Modifications to existing endpoints
3. **Deprecated**: Features scheduled for removal
4. **Removed**: Features no longer available
5. **Fixed**: Bug fixes

Example changelog entry:

.. code-block:: text

    # API Changelog
    
    ## v1.2.0 (2025-03-15)
    
    ### Added
    - Endpoint for bulk booking creation
    - Filtering bookings by service type
    
    ### Changed
    - Expanded instructor availability information in booking responses
    - Improved validation error messages for time conflicts
    
    ### Fixed
    - Fixed issue with timezone handling in booking queries
    
    ## v1.1.0 (2025-01-10)
    
    ### Added
    - Pagination for all list endpoints
    - Search functionality for bookings and clients
    
    ### Deprecated
    - Legacy `/api/bookings/search` endpoint, use query parameters instead
