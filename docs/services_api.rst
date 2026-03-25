Services API Documentation
==========================

This document details the API endpoints available in the services module.

API Authentication
================

All API endpoints in the services module require authentication using JWT (JSON Web Tokens). 

**Authentication Headers**

.. code-block:: text

    Authorization: Bearer <token>

**Obtaining a Token**

.. code-block:: http

    POST /api/auth/token/
    Content-Type: application/json

    {
        "email": "user@example.com",
        "password": "securepassword"
    }

**Response**

.. code-block:: json

    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }

**Token Refresh**

.. code-block:: http

    POST /api/auth/token/refresh/
    Content-Type: application/json

    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }

Organizations
============

List/Create Organizations
------------------------

**GET** ``/services/organizations/``

* Requires staff access
* Lists all organizations with pagination (default: 20 per page)
* Supports filtering by name, location, and status
* Includes contact information and related proposal counts
* Optional query parameters:
  * ``active`` - Filter by active status (true/false)
  * ``location`` - Filter by location name
  * ``search`` - Search across name and address fields

**Example Request**

.. code-block:: http

    GET /services/organizations/
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    Content-Type: application/json

**Example Response**

.. code-block:: json

    {
        "count": 25,
        "next": "/services/organizations/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Acme Corporation",
                "industry": "Technology",
                "contact_email": "contact@acme.com",
                "contact_phone": "+12025550179",
                "address": "123 Main St, San Francisco, CA 94105",
                "employee_count": 500,
                "contract_start_date": "2024-01-15",
                "contract_end_date": "2025-01-14",
                "proposal_count": 3,
                "active_programs": [1, 3],
                "status": "active"
            },
            {
                "id": 2,
                "name": "Global Health Ltd",
                "industry": "Healthcare",
                "contact_email": "info@globalhealth.com",
                "contact_phone": "+12125551098",
                "address": "456 Park Ave, New York, NY 10022",
                "employee_count": 1200,
                "contract_start_date": "2023-10-01",
                "contract_end_date": "2024-09-30",
                "proposal_count": 1,
                "active_programs": [2],
                "status": "active"
            }
        ]
    }

**POST** ``/services/organizations/``

* Requires staff access
* Creates a new organization with validation
* Required fields:
  * ``name`` - Organization name (unique)
  * ``phone_number`` - Must start with '+' and contain at least 10 digits
  * ``address`` - Physical location address
* Optional fields:
  * ``email`` - Valid email format required if provided
  * ``contact_person`` - Primary contact name
  * ``website`` - Valid URL format if provided
  * ``status`` - Default: "Active"

**Example Request**

.. code-block:: http

    POST /services/organizations/
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    Content-Type: application/json

    {
        "name": "New Company Inc",
        "industry": "Finance",
        "contact_email": "contact@newcompany.com",
        "contact_phone": "+14155550123",
        "address": "789 Financial Blvd, Chicago, IL 60601",
        "employee_count": 750,
        "special_requirements": "Requires on-site sessions only"
    }

**Example Success Response**

.. code-block:: json

    {
        "id": 3,
        "name": "New Company Inc",
        "industry": "Finance",
        "contact_email": "contact@newcompany.com",
        "contact_phone": "+14155550123",
        "address": "789 Financial Blvd, Chicago, IL 60601",
        "employee_count": 750,
        "contract_start_date": null,
        "contract_end_date": null,
        "special_requirements": "Requires on-site sessions only",
        "status": "active",
        "created": "2025-03-13T12:45:30Z",
        "modified": "2025-03-13T12:45:30Z"
    }

**Example Error Response**

.. code-block:: json

    {
        "status": "error",
        "code": "validation_error",
        "message": "Invalid data provided",
        "details": {
            "contact_phone": ["Phone number must start with + followed by at least 10 digits."],
            "name": ["An organization with this name already exists."]
        }
    }

**Field Validation Rules**

* ``name``: Required, unique, max length 200 characters
* ``industry``: Required, max length 100 characters
* ``contact_email``: Required, valid email format
* ``contact_phone``: Required, must start with + followed by at least 10 digits
* ``address``: Required, max length 500 characters
* ``employee_count``: Required, must be positive integer
* ``contract_start_date``: Optional, valid date format (YYYY-MM-DD)
* ``contract_end_date``: Optional, must be after contract_start_date if provided
* ``special_requirements``: Optional, no length limit
* ``status``: Optional, must be one of: "active", "inactive", "suspended"

Organization Detail
-----------------

**GET** ``/services/organizations/<id>/``

* Requires staff access
* Returns detailed information about a specific organization
* Includes related proposals, contacts, and corporate programs
* Includes historical booking data and usage statistics

Proposals
========

List/Create Proposals
-------------------

**GET** ``/services/proposals/``

* Requires staff access
* Lists all proposals with pagination
* Supports filtering by organization, status, and date range
* Includes submission date, status, and organization details
* Optional query parameters:
  * ``status`` - Filter by proposal status
  * ``organization_id`` - Filter by specific organization
  * ``date_after`` - Filter proposals submitted after this date
  * ``date_before`` - Filter proposals submitted before this date

**Example Request**

.. code-block:: http

    GET /services/proposals/
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    Content-Type: application/json
    
    {
        "organization_id": 1,
        "status": "sent",
        "date_after": "2024-01-01"
    }

**Example Response**

.. code-block:: json

    {
        "count": 2,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 5,
                "organization": {
                    "id": 1,
                    "name": "Acme Corporation"
                },
                "title": "Q2 Wellness Program",
                "date_submitted": "2024-01-15T10:30:45Z",
                "status": "sent",
                "valid_until": "2024-03-15",
                "programs": [1, 3],
                "created_by": {
                    "id": 2,
                    "name": "Jane Smith"
                }
            },
            {
                "id": 8,
                "organization": {
                    "id": 1,
                    "name": "Acme Corporation"
                },
                "title": "Custom Executive Program",
                "date_submitted": "2024-02-28T14:22:10Z",
                "status": "sent",
                "valid_until": "2024-04-28",
                "programs": [2],
                "created_by": {
                    "id": 3,
                    "name": "Robert Johnson"
                }
            }
        ]
    }

**POST** ``/services/proposals/``

* Requires staff access
* Creates a new proposal with validation
* Required fields:
  * ``organization`` - Valid organization ID
  * ``date_submitted`` - Submission date (cannot be in the future)
  * ``valid_until`` - Expiration date (must be after date_submitted)
  * ``status`` - Initial status (default: "Draft")
* Optional fields:
  * ``description`` - Proposal description
  * ``pricing_details`` - JSON object with pricing structure
  * ``notes`` - Additional notes

**Example Request**

.. code-block:: http

    POST /services/proposals/
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    Content-Type: application/json

    {
        "organization": 1,
        "title": "Fall Wellness Program Proposal",
        "date_submitted": "2025-03-13",
        "programs": [1, 2],
        "custom_services": "10 personalized stretching assessments for executives",
        "pricing_details": {
            "base_price": 5000,
            "per_participant_price": 45,
            "discount": 10,
            "total": 8550
        },
        "valid_until": "2025-05-13",
        "terms_conditions": "Standard terms apply. Valid for 60 days.",
        "status": "draft"
    }

**Field Validation Rules**

* ``organization``: Required, must be a valid organization ID
* ``title``: Required, max length 200 characters
* ``date_submitted``: Required, valid date format (YYYY-MM-DD), cannot be in the future
* ``programs``: Optional but at least one program or custom service required
* ``custom_services``: Optional text field
* ``pricing_details``: Required JSON object with structured pricing information
* ``valid_until``: Required, must be after date_submitted
* ``terms_conditions``: Required, no length limit
* ``status``: Optional, must be one of: "draft", "sent", "accepted", "rejected"

Corporate Programs
================

List/Create Corporate Programs
----------------------------

**GET** ``/services/corporateprograms/``

* Requires staff access
* Lists all corporate programs with pagination
* Supports filtering by organization, status, and activity level
* Includes feature lists, member counts, and utilization metrics
* Optional query parameters:
  * ``organization_id`` - Filter by specific organization
  * ``status`` - Filter by program status
  * ``active`` - Filter by activity status

**Permission Requirements**

* List/view programs: Authenticated user with 'services.view_corporateprogram' permission
* Create/edit programs: Authenticated user with 'services.add_corporateprogram' or 'services.change_corporateprogram' permission
* Delete programs: Authenticated user with 'services.delete_corporateprogram' permission

**Example Request**

.. code-block:: http

    GET /services/corporateprograms/
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    Content-Type: application/json

**Example Response**

.. code-block:: json

    {
        "count": 3,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Executive Wellness Program",
                "description": "Comprehensive wellness program for executives",
                "min_participants": 5,
                "max_participants": 20,
                "services": [
                    {
                        "id": 3,
                        "name": "Executive Wellness Session",
                        "duration": 45
                    },
                    {
                        "id": 7,
                        "name": "Stress Management Workshop",
                        "duration": 60
                    }
                ],
                "organizations_count": 2,
                "created": "2024-01-10T09:15:30Z",
                "modified": "2024-02-15T14:30:45Z"
            },
            {
                "id": 2,
                "name": "Team Building Wellness",
                "description": "Group wellness activities for team building",
                "min_participants": 10,
                "max_participants": 30,
                "services": [
                    {
                        "id": 5,
                        "name": "Group Wellness Session",
                        "duration": 30
                    },
                    {
                        "id": 9,
                        "name": "Team Mobility Workshop",
                        "duration": 45
                    }
                ],
                "organizations_count": 3,
                "created": "2024-01-15T11:30:00Z",
                "modified": "2024-01-15T11:30:00Z"
            }
        ]
    }

Error Responses
=============

**Common Error Response Codes**

* ``400 Bad Request``: Invalid input, validation errors
* ``401 Unauthorized``: Missing or invalid authentication
* ``403 Forbidden``: Authenticated but insufficient permissions
* ``404 Not Found``: Resource not found
* ``409 Conflict``: Resource conflict (e.g., duplicate entry)
* ``429 Too Many Requests``: Rate limit exceeded
* ``500 Internal Server Error``: Server-side error

**Error Response Formats**

For validation errors:

.. code-block:: json

    {
        "status": "error",
        "error_code": "validation_error",
        "message": "The request contains invalid parameters",
        "details": {
            "field_name": ["Specific error message"],
            "another_field": ["Another error message"]
        },
        "resource": "Organization"
    }

For authentication errors:

.. code-block:: json

    {
        "status": "error",
        "error_code": "authentication_required",
        "message": "Authentication credentials were not provided.",
        "details": null,
        "resource": null
    }

For permission errors:

.. code-block:: json

    {
        "status": "error",
        "error_code": "permission_denied",
        "message": "You do not have permission to perform this action.",
        "details": null,
        "resource": "Proposal"
    }

Batch Operations
==============

The API supports batch operations for certain endpoints to improve performance when dealing with multiple resources.

**Batch Create Organizations**

.. code-block:: http

    POST /services/organizations/batch/
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    Content-Type: application/json

    {
        "organizations": [
            {
                "name": "Company A",
                "industry": "Technology",
                "contact_email": "contact@companya.com",
                "contact_phone": "+12025550101",
                "address": "Address A",
                "employee_count": 500
            },
            {
                "name": "Company B",
                "industry": "Healthcare",
                "contact_email": "contact@companyb.com",
                "contact_phone": "+12025550102",
                "address": "Address B",
                "employee_count": 1200
            }
        ]
    }

**Batch Response**

.. code-block:: json

    {
        "created": 2,
        "failed": 0,
        "results": [
            {
                "id": 10,
                "name": "Company A",
                "status": "success"
            },
            {
                "id": 11,
                "name": "Company B",
                "status": "success"
            }
        ]
    }

API Rate Limits
=============

To ensure system stability, the following rate limits apply:

* Anonymous requests: 20 requests per minute
* Authenticated requests: 60 requests per minute
* Batch operations: 5 requests per minute

Rate limit headers are included in all API responses:

.. code-block:: text

    X-RateLimit-Limit: 60
    X-RateLimit-Remaining: 59
    X-RateLimit-Reset: 1584872100
