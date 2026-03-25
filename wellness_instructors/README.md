# Wellness Instructors App

This Django app manages wellness instructors and their sessions for the Wellness Solutions platform.

## Features

- Instructor profiles with specializations and availability
- Session management (one-on-one, group, workshops)
- Automatic instructor profile creation for staff users
- Basic views for listing and viewing instructors and sessions

## Quick Start

1. Add "wellness_instructors" to your INSTALLED_APPS setting:
```python
INSTALLED_APPS = [
    ...
    'wellness_solutions.wellness_instructors',
]
```

2. Include the wellness_instructors URLconf in your project urls.py:
```python
path('instructors/', include('wellness_solutions.wellness_instructors.urls')),
```

3. Run migrations:
```bash
python manage.py migrate
```

## Creating Test Instructors

Use the management command to create test instructors:

```bash
python manage.py create_test_instructor [email] [password] --name "[Full Name]" --specialization [specialization]
```

Example:
```bash
python manage.py create_test_instructor instructor@example.com mypassword --name "John Doe" --specialization flexibility
```

## Available URLs

- `/instructors/` - List all active instructors
- `/instructors/<id>/` - Instructor detail view
- `/instructors/sessions/` - List all active sessions
- `/instructors/sessions/<id>/` - Session detail view
- `/instructors/sessions/create/` - Create new session (instructors only)

## Models

### WellnessInstructor
- Links to User model
- Tracks specializations, certification level, and availability
- Manages instructor profile information

### Session
- Represents wellness sessions
- Supports different session types and difficulty levels
- Tracks capacity and pricing
