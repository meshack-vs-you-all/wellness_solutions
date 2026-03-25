 .. _users:

Users
======================================================================

User Management System
---------------------

The Wellness Solutions implements a robust user management system based on Django's authentication framework with significant extensions for security, role management, and performance.

The custom User model provides flexibility for future enhancements while maintaining compatibility with Django's built-in authorization system.

User Model Features
-----------------

1. **Authentication & Security**
   
   * JWT-based authentication with refresh token support
   * Multi-factor authentication (MFA) with configurable factors
   * Secure email verification with time-limited tokens
   * Password reset with expiring single-use links
   * Comprehensive password policy enforcement
   * Brute-force protection with progressive timeouts
   * Session management with secure timeout controls

2. **Authorization & Roles**
   
   * Hierarchical role system (Admin, Staff, Instructor, Client)
   * Granular permission-based access control
   * Object-level permissions for data security
   * Dynamic role assignment and privilege elevation
   * Audit logging for security-sensitive operations
   * Role-specific dashboard and UI elements

3. **Profile Management**
   
   * Extended user profiles with customizable fields
   * Profile picture and personal information
   * Communication preferences and notification settings
   * Language and locale settings
   * Timezone detection and preference storage
   * Account activity history and session tracking

4. **Relationships & Integration**
   
   * Organization affiliations for corporate users
   * Instructor specialization and certification tracking
   * Booking history and package subscription links
   * Payment method storage with secure tokenization
   * Social authentication integration (optional)
   * External calendar system synchronization

Security Implementation
---------------------

1. **Password Security**
   
   * Passwords stored using Django's PBKDF2 with SHA256
   * Configurable password complexity requirements
   * Password rotation policies with history checking
   * Automatic account locking after failed attempts
   * Secure password recovery workflow

2. **Data Protection**
   
   * Sensitive personal information encrypted at rest
   * PII (Personally Identifiable Information) handling compliant with GDPR
   * Data access logging and monitoring
   * User consent tracking for privacy regulations
   * Data retention policies with scheduled anonymization

User API Endpoints
----------------

1. **Registration & Authentication**
   
   * ``/api/auth/register/`` - User registration with validation
   * ``/api/auth/login/`` - Token-based authentication
   * ``/api/auth/token/refresh/`` - JWT token refresh
   * ``/api/auth/password/reset/`` - Password reset flow
   * ``/api/auth/mfa/setup/`` - Multi-factor authentication setup

2. **Profile Management**
   
   * ``/api/users/profile/`` - User profile CRUD operations
   * ``/api/users/preferences/`` - User preferences management
   * ``/api/users/avatar/`` - Profile picture upload and management
   * ``/api/users/activity/`` - Account activity history

3. **Administrative**
   
   * ``/api/users/`` - Admin-only user management
   * ``/api/users/roles/`` - Role assignment and management
   * ``/api/users/permissions/`` - Permission configuration
   * ``/api/users/audit/`` - Security audit logging

Form Validation
-------------

All user-related forms implement comprehensive validation including:

* Email format and uniqueness verification
* Username format and availability checking
* Password strength enforcement with helpful feedback
* Cross-field validation for related fields
* Custom error messages for usability

The validation logic follows the project's field validation guidelines with exhaustive testing for edge cases.

.. automodule:: users.models
   :members:
   :undoc-members:
   :show-inheritance:
