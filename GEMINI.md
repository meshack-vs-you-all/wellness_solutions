# Wellness Solutions

## Project Overview

This project is a comprehensive web application for a stretching and fitness studio, named "Wellness Solutions". It's built with a backend powered by Django and a frontend using React. The application seems to handle bookings, payments, and user management.

### Backend (Django)

The backend is a Django project, structured using the `cookiecutter-django` template. It includes features like user authentication, Celery for asynchronous tasks, and a REST API likely built with Django REST Framework. The project emphasizes code quality with tools like `pytest` for testing, `mypy` for type checking, and `ruff` for linting.

### Frontend (React)

The frontend is a React application built with Vite. It uses `axios` for making API calls to the Django backend, `react-router-dom` for navigation, and `recharts` for displaying data visualizations. The styling is done using `tailwindcss`.

## User Management

The project has a comprehensive user management system that is built on top of Django's authentication framework. The system includes features like JWT-based authentication, multi-factor authentication, role-based access control, and detailed user profiles.

For a detailed explanation of the user management system, please refer to the `docs/users.rst` file.


## Bookings

The project has a comprehensive bookings module that allows for the management of client appointments, scheduling, and calendar management. The system includes features like appointment creation, resource availability checking, automatic reminders, and calendar integration.

For a detailed explanation of the bookings module, please refer to the `docs/bookings.rst` file.





### Backend

1.  **Install dependencies:**
    ```bash
    pip install -r requirements/local.txt
    ```

2.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

3.  **Run the development server:**
    The development server can be started with the following command. It will be accessible at `http://127.0.0.1:8000`.
    ```bash
    python manage.py runserver
    ```
    The local settings enable `django-debug-toolbar` and `django-browser-reload` for a better development experience.

4.  **Run Celery worker (for asynchronous tasks):**
    To process asynchronous tasks, run the Celery worker in a separate terminal:
    ```bash
    celery -A config.celery_app worker -l info
    ```
    In the local environment, Celery is configured for eager propagation of tasks.

5.  **Email Server:**
    The project uses `mailpit` as a local SMTP server. To view emails sent by the application, open your browser and go to `http://127.0.0.1:8025`.


### Frontend

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    The development server will be accessible at `http://localhost:5173`.
    ```bash
    npm run dev
    ```

## Testing

The project has a comprehensive testing guide that covers the testing philosophy, types of tests, testing tools, and best practices. The project uses `pytest` for testing and aims for high code coverage.

For a detailed explanation of the testing guidelines, please refer to the `docs/testing.rst` file.


## Documentation

The project has a comprehensive set of documentation that is built with Sphinx. The documentation is written in reStructuredText and can be found in the `docs` directory. The project also uses `sphinx-apidoc` to automatically generate documentation from docstrings.

For a detailed explanation of how to build and contribute to the documentation, please refer to the `docs/howto.rst` file.




## Contributing

The project has a comprehensive contributing guide that outlines the development process, coding standards, and pull request process. All contributions should be associated with an issue and follow the feature branch workflow. The project uses `pytest` for testing and `ruff` and `djlint` for code style.

For a detailed explanation of how to contribute, please refer to the `docs/contributing.rst` file.

## API Guidelines

The project has a detailed set of API guidelines that cover design principles, URL structure, HTTP methods, request/response formats, error handling, and more. The API is versioned and uses JWT for authentication.

For a detailed explanation of the API guidelines, please refer to the `docs/api_guidelines.rst` file.





## Deployment

The project has a comprehensive deployment guide that covers the different environments, the infrastructure setup, the CI/CD pipeline, and more. The application is deployed on AWS and uses Docker for containerization.

For a detailed explanation of the deployment process, please refer to the `docs/deployment.rst` file.


## Services API

The project has a comprehensive services API that allows for the management of organizations, proposals, and corporate programs. The API is authenticated using JWT and includes features like filtering, sorting, and pagination.

## Packages

The project has a comprehensive packages module that allows for the management of service packages. The system includes features like package creation, client assignment, usage tracking, and expiration handling.

For a detailed explanation of the packages module, please refer to the `docs/packages.rst` file.


