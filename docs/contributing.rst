Contributing Guide
=================

Thank you for your interest in contributing to the Wellness Solutions project! This guide will help you understand our development process and how you can effectively contribute to the project.

Code of Conduct
--------------

Our team is committed to fostering an open and welcoming environment. By participating in this project, you agree to abide by our code of conduct:

* Treat all individuals with respect and kindness
* Use inclusive language and be considerate of differing viewpoints
* Gracefully accept constructive criticism
* Focus on what is best for the community
* Show empathy towards other community members

Development Process
-----------------

Issue Tracking
~~~~~~~~~~~~

All work on the Wellness Solutions project should be associated with an issue in our issue tracker. Issues fall into these categories:

* **Bug**: Something isn't working as expected
* **Feature**: A new capability or enhancement
* **Technical Debt**: Infrastructure or code quality improvements
* **Documentation**: Documentation improvements or additions

Before starting work:
1. Check if an issue already exists for your contribution
2. If not, create a new issue describing what you want to work on
3. Assign the issue to yourself or request assignment from a maintainer

Git Workflow
~~~~~~~~~~

We follow a feature branch workflow:

1. Fork the repository (if you're an external contributor)
2. Create a feature branch from `develop`:

.. code-block:: bash

    git checkout develop
    git pull
    git checkout -b feature/issue-{issue-number}-brief-description

3. Make your changes, following the coding standards
4. Commit your changes with descriptive commit messages:

.. code-block:: bash

    git add .
    git commit -m "Type: Description of changes [Fixes #issue-number]"

   Where `Type` is one of:
   * `Fix`: Bug fix
   * `Feat`: New feature
   * `Docs`: Documentation changes
   * `Style`: Formatting, missing semicolons, etc; no code change
   * `Refactor`: Code refactoring without changing functionality
   * `Test`: Adding missing tests
   * `Chore`: Maintenance tasks, dependency updates, etc.

5. Push your changes to your fork:

.. code-block:: bash

    git push origin feature/issue-{issue-number}-brief-description

6. Create a pull request to the `develop` branch of the main repository

Pull Request Process
~~~~~~~~~~~~~~~~~~

When submitting a pull request:

1. Provide a clear description of the changes
2. Reference the issue number using `Fixes #issue-number` or `Relates to #issue-number`
3. Ensure all automated tests pass
4. Make sure your code follows the project's coding standards
5. Include any necessary documentation updates
6. Request review from at least one maintainer

Code Reviews
~~~~~~~~~~~

All submissions require review before being merged:

* Be responsive to feedback and willing to make requested changes
* Keep discussions focused on the code, not personal preferences
* If you disagree with a suggestion, explain your reasoning clearly
* Remember that code reviews are about improving the codebase, not criticizing the contributor

Coding Standards
--------------

Python Style Guide
~~~~~~~~~~~~~~~~

We follow a modified version of PEP 8:

* Use 4 spaces for indentation
* Maximum line length of 100 characters
* Use docstrings for all classes and functions
* Use type hints where appropriate
* Name variables and functions in `snake_case`
* Name classes in `PascalCase`
* Add appropriate comments for complex code sections

Here's an example:

.. code-block:: python

    def calculate_availability(instructor: WellnessInstructor, start_date: date, end_date: date) -> dict:
        """
        Calculate instructor availability within the given date range.
        
        Args:
            instructor: The instructor to check availability for
            start_date: The start date of the range
            end_date: The end date of the range
            
        Returns:
            A dictionary mapping dates to availability status
        """
        result = {}
        
        # Logic to calculate availability
        # ...
        
        return result

JavaScript Style Guide
~~~~~~~~~~~~~~~~~~~~

For JavaScript code:

* Use 2 spaces for indentation
* Use semicolons at the end of statements
* Use camelCase for variables and functions
* Add JSDoc comments for functions
* Use ES6+ features where appropriate

Testing Requirements
-----------------

All new features and bug fixes should include tests:

* Write unit tests for individual functions and methods
* Write integration tests for API endpoints
* Ensure existing tests pass with your changes
* Aim for at least 80% code coverage for new code

Running tests:

.. code-block:: bash

    # Run all tests
    pytest
    
    # Run with coverage
    pytest --cov=wellness_solutions
    
    # Run specific tests
    pytest wellness_solutions/module_name/tests/test_specific.py::TestClass::test_function

Documentation Standards
---------------------

All features should be documented:

* Add docstrings to all classes and functions
* Update or create module-level documentation in the `docs/` directory
* Document API endpoints with expected request/response formats
* Include examples where helpful

Documentation uses reStructuredText format and is built with Sphinx:

.. code-block:: bash

    # Install documentation dependencies
    pip install -r requirements/docs.txt
    
    # Build the documentation
    cd docs
    make html

Working with Dependencies
----------------------

Adding Dependencies
~~~~~~~~~~~~~~~~

To add a new dependency:

1. Add it to the appropriate requirements file:
   * `requirements/base.txt` for core dependencies
   * `requirements/local.txt` for development-only dependencies
   * `requirements/production.txt` for production-only dependencies

2. Include a comment explaining why the dependency is needed:

.. code-block:: text

    # PDF generation library
    reportlab==3.6.9

3. Update the dependency documentation in the README if necessary

Security Considerations
---------------------

* Never commit sensitive information (tokens, passwords, etc.)
* Use environment variables for configuration
* Follow security best practices in your code:
  * Validate user input
  * Use parameterized queries
  * Implement proper authentication and authorization
  * Sanitize data output to prevent XSS attacks

Reporting Security Issues
~~~~~~~~~~~~~~~~~~~~~~~

For security issues, please do not create a public issue. Instead, email security@jpfstretch.com with details about the vulnerability.

Submitting Feature Requests
-------------------------

To suggest a new feature:

1. Check if the feature has already been requested
2. Create a new issue with the 'Feature' label
3. Clearly describe the feature and its benefits
4. Include any relevant mockups or examples
5. Be prepared to discuss the feature with maintainers

Release Process
-------------

We follow semantic versioning (MAJOR.MINOR.PATCH):

* MAJOR version for incompatible API changes
* MINOR version for new functionality in a backward-compatible manner
* PATCH version for backward-compatible bug fixes

Releases are created from the `main` branch after features and fixes from `develop` have been tested and approved.

Getting Help
----------

If you need help with the contribution process:

* Ask questions in the project's Slack channel (#stretch-hub-dev)
* Reach out to maintainers directly
* Email the development team at dev@jpfstretch.com

Thank you for contributing to Wellness Solutions!
