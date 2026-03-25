# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Wellness Solutions is a comprehensive Django web application for managing bookings, payments, and user management at a stretching and fitness studio. Built using cookiecutter-django with modern Django patterns and best practices.

## Essential Development Commands

### Initial Setup and Environment
```bash
# Set up local development with Docker
docker-compose -f docker-compose.local.yml up --build

# Run Django development server without Docker
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate
```

### Testing and Quality Assurance
```bash
# Run all tests
pytest

# Run tests with coverage
coverage run -m pytest
coverage html
# View coverage report: open htmlcov/index.html

# Run specific test
pytest path/to/test_file.py::TestClassName::test_method_name

# Type checking
mypy wellness_solutions

# Code formatting and linting
ruff check .
ruff format .

# Template linting
djlint --check .
djlint --reformat .
```

### Celery Background Tasks
```bash
# Start Celery worker
celery -A config.celery_app worker -l info

# Start Celery beat scheduler
celery -A config.celery_app beat

# Start worker with beat (development only)
celery -A config.celery_app worker -B -l info

# Monitor tasks with Flower (available at http://127.0.0.1:5555)
celery -A config.celery_app flower
```

### Database Operations
```bash
# Database shell
python manage.py dbshell

# Django shell with extensions
python manage.py shell_plus

# Create database backup
python manage.py dumpdata > backup.json

# Load database from backup
python manage.py loaddata backup.json
```

## Architecture Overview

### Core Application Structure

This is a Django project organized into multiple specialized apps:

- **bookings/**: Core booking system managing wellness sessions, payments, and scheduling
- **clients/**: Client profile management and session tracking 
- **users/**: Extended user management with authentication
- **services/**: Service catalog and organization management
- **packages/**: Package/membership management system
- **locations/**: Multi-location support with location-specific services
- **wellness_instructors/**: Instructor management and scheduling
- **schedules/**: Session scheduling and availability management
- **theme/**: Custom theming and UI components
- **docs/**: Documentation system

### Key Design Patterns

**Domain-Driven Design**: Each app represents a distinct business domain with its own models, views, and business logic. Apps communicate through well-defined interfaces and foreign key relationships.

**Service Layer Pattern**: Business logic is encapsulated in dedicated service modules rather than being scattered across views and models.

**Event-Driven Architecture**: Uses Django signals and Celery tasks for decoupled event handling (notifications, email sending, booking confirmations).

**Multi-Tenant Design**: Supports multiple organizations/locations through the `Organization` and `Location` models.

### Data Model Relationships

The core entity relationships flow like this:
- `User` → `ClientProfile` (one-to-one)
- `Location` → `LocationService`, `LocationInstructor` (location-specific offerings)
- `Booking` connects `User`, `Location`, `LocationService`, `LocationInstructor`
- `Package` → `ClientPackage` (user package ownership)
- `Booking` can optionally link to `Package` for credits

### API Architecture

**REST API**: Built with Django REST Framework
- ViewSets in `api_router.py` for standard CRUD operations
- Custom API endpoints in `api_views.py` for specialized functionality
- API documentation available via DRF Spectacular at `/api/docs/`

**Authentication**: 
- Django Allauth with MFA support
- Token-based authentication for API access
- Role-based permissions system

### Background Processing

**Celery Integration**: 
- Task queue for email notifications, booking confirmations, and scheduled operations
- Redis as message broker and result backend
- Separate worker and beat containers in Docker setup

## Development Environment

### Docker Development Setup
The project uses Docker Compose for local development:

- **django**: Main application server (port 8000)
- **postgres**: PostgreSQL database (port 5432) 
- **redis**: Cache and Celery broker (port 6379)
- **celeryworker**: Background task processor
- **celerybeat**: Scheduled task manager
- **flower**: Task monitoring UI (port 5555)
- **mailpit**: Email testing server (port 8025)

### Settings Structure
Django settings are environment-specific:
- `config.settings.local`: Development settings
- `config.settings.production`: Production settings  
- `config.settings.test`: Test-specific settings

### Key Configuration Files
- `pyproject.toml`: Tool configuration (pytest, mypy, ruff, djlint)
- `requirements/`: Split requirements files for different environments
- `.pre-commit-config.yaml`: Git hooks for code quality

## Testing Strategy

- **pytest** as the test runner with Django integration
- **factory-boy** for test data generation
- **coverage** for test coverage reporting
- Tests should be placed alongside the code they test (`tests/` directories in each app)
- Model tests focus on validation and business logic
- API tests use DRF's test client
- Integration tests cover cross-app functionality

## Security Considerations

The application implements several security measures:
- CSRF protection enabled
- Rate limiting on critical endpoints
- Input sanitization with bleach
- Proper permission systems for different user roles
- Environment-specific security settings

## Common Development Patterns

### Adding a New App
1. Create app with `python manage.py startapp appname`
2. Add to `INSTALLED_APPS` in settings
3. Create `urls.py` and add to main `config/urls.py`
4. Follow the existing app structure (models, views, serializers, etc.)

### Database Changes
1. Always create migrations: `python manage.py makemigrations`
2. Review migration files before applying
3. Test migrations on a copy of production data when possible
4. Consider data migrations for complex changes

### API Development
1. Use ViewSets for standard CRUD operations
2. Custom endpoints should go in `api_views.py`
3. Always add appropriate permissions
4. Document new endpoints in the API schema

## Deployment Notes

- Uses Docker for containerized deployment
- Supports both local development and production configurations
- Static files handled by WhiteNoise
- Media files should be served by a proper web server in production
- Celery workers and beat scheduler run as separate containers

## Monitoring and Debugging

- **Django Debug Toolbar**: Available in development mode
- **Flower**: Celery task monitoring at http://127.0.0.1:5555
- **Mailpit**: Email testing at http://127.0.0.1:8025  
- **Sentry**: Error tracking (configure DSN for production)
- **Logging**: Configured through Django settings, outputs to console in development
