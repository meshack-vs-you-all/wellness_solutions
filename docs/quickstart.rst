Quick Start Guide
===============

Welcome to the Wellness Solutions project! This quick start guide will help you set up your development environment and get familiar with the project structure and workflows.

Environment Setup
----------------

Prerequisites
~~~~~~~~~~~~

Before you begin, ensure you have the following installed:

* Python 3.8+
* PostgreSQL 13+
* Redis 6+
* Git
* Node.js 14+ and npm (for frontend components)

Clone the Repository
~~~~~~~~~~~~~~~~~~

Clone the Wellness Solutions repository:

.. code-block:: bash

    git clone https://github.com/jpf/stretch-hub.git
    cd stretch-hub

Virtual Environment Setup
~~~~~~~~~~~~~~~~~~~~~~~

Create and activate a virtual environment:

.. code-block:: bash

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies
~~~~~~~~~~~~~~~~~~

Install the required Python packages:

.. code-block:: bash

    pip install -r requirements/local.txt

Database Setup
~~~~~~~~~~~~

1. Create a PostgreSQL database:

.. code-block:: bash

    createdb wellness_solutions

2. Set up environment variables in a `.env` file:

.. code-block:: bash

    touch .env
    echo "DATABASE_URL=postgres://postgres:postgres@localhost:5432/wellness_solutions" >> .env
    echo "REDIS_URL=redis://localhost:6379/0" >> .env

3. Run migrations:

.. code-block:: bash

    python manage.py migrate

4. Create a superuser:

.. code-block:: bash

    python manage.py createsuperuser

Running the Development Server
----------------------------

Start the development server:

.. code-block:: bash

    python manage.py runserver

The application will be available at http://127.0.0.1:8000/.

Project Structure
---------------

Key Directories
~~~~~~~~~~~~~

* `config/` - Django settings and configuration files
* `wellness_solutions/` - Main Python package containing all application code
  * `users/` - User authentication and profile management
  * `locations/` - Location and facility management
  * `bookings/` - Booking and appointment scheduling
  * `packages/` - Service package management
  * `wellness_instructors/` - Instructor profile and availability management
  * `schedules/` - Calendar and scheduling system
  * `payments/` - Payment processing and financial management
* `docs/` - Project documentation
* `static/` - Static files (CSS, JS, images)
* `templates/` - HTML templates

Development Workflow
------------------

Code Quality Standards
~~~~~~~~~~~~~~~~~~~~

Before submitting code, ensure it meets our quality standards:

1. **Field Validation**: Implement comprehensive field validation for all models
2. **Error Handling**: Use appropriate try-except blocks and provide clear error messages
3. **Code Duplication**: Check for and refactor any duplicate code
4. **Template Consistency**: Maintain consistent template structure and block naming
5. **Database Integrity**: Use appropriate model constraints and indexes
6. **Testing**: Write tests for all new features and ensure existing tests pass

Running Tests
~~~~~~~~~~~

Run the test suite:

.. code-block:: bash

    pytest

To run tests with coverage:

.. code-block:: bash

    pytest --cov=wellness_solutions

Code Formatting
~~~~~~~~~~~~~

Format your code with Black:

.. code-block:: bash

    black .

Lint your code with flake8:

.. code-block:: bash

    flake8

Git Workflow
~~~~~~~~~~

We follow a feature branch workflow:

1. Create a feature branch from `develop`:

.. code-block:: bash

    git checkout develop
    git pull
    git checkout -b feature/your-feature-name

2. Make changes and commit them:

.. code-block:: bash

    git add .
    git commit -m "Descriptive commit message"

3. Push your branch and create a pull request:

.. code-block:: bash

    git push -u origin feature/your-feature-name

API Development
-------------

RESTful API Basics
~~~~~~~~~~~~~~~~

The Wellness Solutions uses Django REST Framework for API development. Key points:

* All endpoints use JWT authentication
* API namespaced under `/api/v1/`
* Request/response format is JSON
* Comprehensive validation with descriptive error messages

Creating a New Endpoint
~~~~~~~~~~~~~~~~~~~~~

1. Define serializers in `serializers.py`
2. Create viewsets in `views.py`
3. Register routes in `urls.py`
4. Add tests in `tests/test_api.py`
5. Document the API in the appropriate RST file

Example:

.. code-block:: python

    # serializers.py
    from rest_framework import serializers
    from .models import YourModel

    class YourModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = YourModel
            fields = ["id", "name", "description"]
            
    # views.py
    from rest_framework import viewsets
    from .models import YourModel
    from .serializers import YourModelSerializer

    class YourModelViewSet(viewsets.ModelViewSet):
        queryset = YourModel.objects.all()
        serializer_class = YourModelSerializer
        
    # urls.py
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
    from .views import YourModelViewSet
    
    router = DefaultRouter()
    router.register("your-models", YourModelViewSet)
    
    urlpatterns = [
        path("", include(router.urls)),
    ]

Frontend Development
------------------

The frontend uses a combination of Django templates and JavaScript with some Vue.js components.

Key Components:
* Bootstrap 5 for responsive styling
* Vue.js for interactive components
* Axios for API requests

Building Frontend Assets
~~~~~~~~~~~~~~~~~~~~~~

Install npm dependencies:

.. code-block:: bash

    npm install

Run the build process:

.. code-block:: bash

    npm run build

Or watch for changes during development:

.. code-block:: bash

    npm run dev

Database Migrations
-----------------

Creating Migrations
~~~~~~~~~~~~~~~~~

After modifying models, create migrations:

.. code-block:: bash

    python manage.py makemigrations

Applying Migrations
~~~~~~~~~~~~~~~~~

Apply pending migrations:

.. code-block:: bash

    python manage.py migrate

Deployment
---------

We use Docker for production deployments. To build the Docker image:

.. code-block:: bash

    docker-compose build
    docker-compose up -d

For detailed deployment instructions, see the [Deployment Guide](deployment.rst).

Getting Help
-----------

* Check the [project documentation](https://jpf-stretch-hub.readthedocs.io/)
* Join the Slack channel #stretch-hub-dev
* Email the development team at dev@jpfstretch.com

Next Steps
---------

Now that you're set up, explore these resources:

* [Architecture Overview](architecture.rst) - Understand the system design
* [API Guidelines](api_guidelines.rst) - Learn our API design principles
* [Contributing Guide](contributing.rst) - How to contribute to the project
* [Module Documentation](users.rst) - Detailed documentation for each module
