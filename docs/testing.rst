Testing Guide
============

This guide outlines testing requirements, practices, and tools used in the Wellness Solutions project to ensure code quality and prevent regressions.

Testing Philosophy
----------------

Quality is a fundamental requirement for the Wellness Solutions platform. Our testing approach is guided by these principles:

1. **Comprehensive Coverage**: Test all critical code paths and business logic
2. **Shift Left**: Find issues as early as possible in the development cycle
3. **Automation First**: Automate tests whenever possible
4. **Test Pyramid**: Balance unit, integration, and end-to-end tests
5. **Quality Gates**: No code moves to production without passing all tests

Types of Tests
------------

Unit Tests
~~~~~~~~~

Unit tests verify that individual components (functions, methods, classes) work correctly in isolation:

* Test individual functions and methods
* Mock external dependencies
* Focus on edge cases and validation logic
* Fast execution (milliseconds per test)

Example Unit Test:

.. code-block:: python

    def test_calculate_booking_duration():
        """Test that booking duration is calculated correctly."""
        start_time = timezone.datetime(2025, 3, 15, 14, 0)
        end_time = timezone.datetime(2025, 3, 15, 15, 30)
        
        booking = Booking(start_time=start_time, end_time=end_time)
        
        self.assertEqual(booking.get_duration_minutes(), 90)
        
    def test_validate_booking_times():
        """Test validation logic for booking times."""
        # Test valid times
        start_time = timezone.now() + timezone.timedelta(days=1)
        end_time = start_time + timezone.timedelta(hours=1)
        
        booking = Booking(start_time=start_time, end_time=end_time)
        booking.clean()  # Should not raise exception
        
        # Test invalid times (end before start)
        start_time = timezone.now() + timezone.timedelta(days=1)
        end_time = start_time - timezone.timedelta(hours=1)
        
        booking = Booking(start_time=start_time, end_time=end_time)
        with self.assertRaises(ValidationError):
            booking.clean()

Integration Tests
~~~~~~~~~~~~~~~

Integration tests verify that multiple components work together correctly:

* Test interactions between components
* Focus on API endpoints and database operations
* Include serialization, validation, and permissions
* Moderate execution speed (hundreds of milliseconds per test)

Example Integration Test:

.. code-block:: python

    def test_create_booking_api():
        """Test the booking creation API."""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('api:bookings-list')
        data = {
            'client': self.client_user.id,
            'service': self.service.id,
            'location': self.location.id,
            'instructor': self.instructor.id,
            'start_time': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
            'end_time': (timezone.now() + timezone.timedelta(days=1, hours=1)).isoformat(),
            'notes': 'Test booking'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        
        booking = Booking.objects.first()
        self.assertEqual(booking.client, self.client_user)
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.status, 'pending')

End-to-End Tests
~~~~~~~~~~~~~~

End-to-end tests verify that complete user flows work as expected:

* Test entire user journeys
* Include frontend and backend components
* Focus on user-facing functionality
* Slower execution (seconds per test)

Example End-to-End Test (using Selenium):

.. code-block:: python

    def test_book_appointment_flow(self):
        """Test the entire appointment booking flow."""
        # Log in
        self.browser.get(self.live_server_url + '/login/')
        self.browser.find_element_by_name('username').send_keys('client@example.com')
        self.browser.find_element_by_name('password').send_keys('password123')
        self.browser.find_element_by_css_selector('button[type="submit"]').click()
        
        # Navigate to booking page
        self.browser.get(self.live_server_url + '/bookings/new/')
        
        # Select service
        select = Select(self.browser.find_element_by_name('service'))
        select.select_by_visible_text('Deep Tissue Stretch')
        
        # Select location
        select = Select(self.browser.find_element_by_name('location'))
        select.select_by_visible_text('Downtown Studio')
        
        # Select date and time
        # (Implementation depends on date picker component)
        date_input = self.browser.find_element_by_name('date')
        date_input.clear()
        date_input.send_keys('2025-05-15')
        
        select = Select(self.browser.find_element_by_name('time'))
        select.select_by_visible_text('2:00 PM')
        
        # Submit booking
        self.browser.find_element_by_css_selector('button[type="submit"]').click()
        
        # Verify success
        success_message = self.browser.find_element_by_css_selector('.alert-success')
        self.assertIn('Booking confirmed', success_message.text)
        
        # Verify database record
        booking = Booking.objects.last()
        self.assertEqual(booking.service.name, 'Deep Tissue Stretch')
        self.assertEqual(booking.location.name, 'Downtown Studio')
        self.assertEqual(booking.start_time.date(), datetime.date(2025, 5, 15))

Testing Tools
-----------

Wellness Solutions uses these testing tools:

* **pytest**: Primary test runner
* **django-test-plus**: Utilities for Django testing
* **factory_boy**: Test data generation
* **coverage.py**: Code coverage measurement
* **selenium**: Browser automation for end-to-end tests
* **pytest-mock**: Mocking for unit tests
* **freezegun**: Date/time mocking

Setting Up the Test Environment
-----------------------------

Local Test Setup
~~~~~~~~~~~~~~

To set up your local test environment:

1. Install test dependencies:

.. code-block:: bash

    pip install -r requirements/test.txt

2. Configure test settings:

.. code-block:: bash

    export DJANGO_SETTINGS_MODULE=config.settings.test

3. Run the tests:

.. code-block:: bash

    pytest

Test Configuration
~~~~~~~~~~~~~~~~

The test settings are defined in `config/settings/test.py` and include:

* SQLite database for faster test execution
* Disabled Celery task execution (tasks run synchronously)
* Test-specific cache backend
* Simplified password hashing for faster tests
* Disabled CSRF protection for API tests

Writing Effective Tests
---------------------

Test Case Organization
~~~~~~~~~~~~~~~~~~~~

Organize tests following these guidelines:

* Group tests by functionality and module
* Use descriptive test class and method names
* Follow naming convention: `test_<what is being tested>_<expected outcome>`
* Keep test methods focused on testing one thing

For example:

.. code-block:: python

    class BookingModelTests(TestCase):
        """Tests for the Booking model."""
        
        def test_duration_calculation_returns_correct_minutes(self):
            """Test that duration is calculated correctly in minutes."""
            # Test implementation
            
        def test_overlapping_booking_validation_raises_error(self):
            """Test that overlapping bookings are rejected."""
            # Test implementation

    class BookingAPITests(APITestCase):
        """Tests for the Booking API endpoints."""
        
        def test_authenticated_user_can_create_booking(self):
            """Test that authenticated users can create bookings."""
            # Test implementation
            
        def test_unauthenticated_user_cannot_create_booking(self):
            """Test that unauthenticated users cannot create bookings."""
            # Test implementation

Test Data Management
~~~~~~~~~~~~~~~~~

Use factories to create test data:

.. code-block:: python

    import factory
    from factory.django import DjangoModelFactory
    
    class UserFactory(DjangoModelFactory):
        class Meta:
            model = get_user_model()
            
        email = factory.Sequence(lambda n: f'user{n}@example.com')
        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
        is_active = True
        
    class InstructorFactory(DjangoModelFactory):
        class Meta:
            model = WellnessInstructor
            
        user = factory.SubFactory(UserFactory)
        bio = factory.Faker('paragraph')
        experience_years = factory.Faker('random_int', min=1, max=20)

Fixtures for common test scenarios:

.. code-block:: python

    @pytest.fixture
    def instructor_with_schedule():
        """Create an instructor with a defined schedule."""
        instructor = InstructorFactory()
        
        # Create default schedule
        schedule = Schedule.objects.create(
            content_object=instructor,
            name=f"{instructor.user.get_full_name()} Schedule"
        )
        
        # Add recurring events (Monday-Friday, 9 AM - 5 PM)
        for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
            RecurringEvent.objects.create(
                schedule=schedule,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0)
            )
            
        return instructor

Field Validation Testing
~~~~~~~~~~~~~~~~~~~~~

As per our code quality rules, thoroughly test field validation:

.. code-block:: python

    def test_booking_field_validation(self):
        """Test comprehensive field validation for Booking model."""
        # Test required fields
        booking = Booking()
        with self.assertRaises(ValidationError) as context:
            booking.full_clean()
            
        errors = context.exception.message_dict
        self.assertIn('client', errors)
        self.assertIn('service', errors)
        self.assertIn('start_time', errors)
        self.assertIn('end_time', errors)
        
        # Test data types
        booking = Booking(
            client=self.client_user,
            service=self.service,
            start_time="invalid-date",  # Invalid date format
            end_time=timezone.now()
        )
        with self.assertRaises(ValidationError) as context:
            booking.full_clean()
            
        errors = context.exception.message_dict
        self.assertIn('start_time', errors)
        
        # Test value constraints
        booking = Booking(
            client=self.client_user,
            service=self.service,
            start_time=timezone.now() - timezone.timedelta(days=1),  # Past date
            end_time=timezone.now()
        )
        with self.assertRaises(ValidationError) as context:
            booking.full_clean()
            
        errors = context.exception.message_dict
        self.assertIn('start_time', errors)
        
        # Test foreign key relationships
        non_existent_id = User.objects.order_by('-id').first().id + 1
        booking = Booking(
            client_id=non_existent_id,  # Non-existent user
            service=self.service,
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=1, hours=1)
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

Edge Case Testing
~~~~~~~~~~~~~~~

Identify and test edge cases:

* Boundary values (min/max, empty/full)
* Unusual inputs (special characters, very long text)
* Race conditions and concurrent operations
* Resource limitations (memory, file handles)
* System transitions (status changes, workflows)

Example:

.. code-block:: python

    def test_booking_edge_cases(self):
        """Test edge cases for booking creation."""
        # Test booking at exact opening time
        location = LocationFactory(
            operating_hours={"monday": {"open": "09:00", "close": "17:00"}}
        )
        
        monday = next_weekday(timezone.now(), 0)  # Get next Monday
        opening_time = datetime.combine(monday, time(9, 0))
        closing_time = datetime.combine(monday, time(17, 0))
        
        # At opening time should be valid
        booking = Booking(
            client=self.client_user,
            service=self.service,
            location=location,
            start_time=opening_time,
            end_time=opening_time + timezone.timedelta(hours=1)
        )
        booking.full_clean()  # Should not raise error
        
        # Right at closing time should be invalid
        booking = Booking(
            client=self.client_user,
            service=self.service,
            location=location,
            start_time=closing_time - timezone.timedelta(hours=1),
            end_time=closing_time + timezone.timedelta(minutes=1)
        )
        with self.assertRaises(ValidationError):
            booking.full_clean()

Test Mocking
~~~~~~~~~~

Use mocking to isolate the unit under test:

.. code-block:: python

    @patch('payments.gateways.stripe_gateway.stripe.Charge.create')
    def test_payment_processing(self, mock_charge_create):
        """Test payment processing with mocked Stripe API."""
        # Configure the mock
        mock_charge_create.return_value = {
            'id': 'ch_test123',
            'status': 'succeeded',
            'amount': 5000,
            'currency': 'usd'
        }
        
        # Create payment
        payment = Payment(
            amount=50.00,
            currency='USD',
            payment_method='credit_card',
            description='Test payment'
        )
        
        # Process payment
        success, message = payment.process_payment()
        
        # Verify outcome
        self.assertTrue(success)
        self.assertEqual(payment.status, 'completed')
        self.assertEqual(payment.transaction_id, 'ch_test123')
        
        # Verify mock was called correctly
        mock_charge_create.assert_called_once_with(
            amount=5000,  # Cents
            currency='usd',
            description='Test payment',
            source=ANY
        )

Test for Error Handling
~~~~~~~~~~~~~~~~~~~~~

Following our error handling guidelines, test error scenarios thoroughly:

.. code-block:: python

    def test_error_handling_in_booking_creation(self):
        """Test error handling during booking creation."""
        with patch('bookings.models.Booking.save') as mock_save:
            # Simulate database error
            mock_save.side_effect = IntegrityError("Duplicate key value violates unique constraint")
            
            url = reverse('api:bookings-list')
            data = {
                'client': self.client_user.id,
                'service': self.service.id,
                'location': self.location.id,
                'instructor': self.instructor.id,
                'start_time': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
                'end_time': (timezone.now() + timezone.timedelta(days=1, hours=1)).isoformat()
            }
            
            response = self.client.post(url, data, format='json')
            
            # Check response
            self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
            self.assertEqual(response.data['code'], 'database_error')
            self.assertIn('message', response.data)

Code Coverage
-----------

We aim for high code coverage, but focus on meaningful coverage:

* Minimum coverage threshold: 80% for all modules
* Critical paths should have 100% coverage
* Cover both success and error paths
* Check coverage reports for missed branches

Running tests with coverage:

.. code-block:: bash

    pytest --cov=wellness_solutions

View coverage report:

.. code-block:: bash

    coverage report -m
    
    # For HTML report
    coverage html
    # Then open htmlcov/index.html

Continuous Integration
-------------------

Automated testing is integrated into our CI/CD pipeline:

* Tests run on every pull request
* Tests run on every push to develop and main branches
* Code coverage reports generated automatically
* Linting and static analysis included in pipeline
* Required status checks must pass before merging

Test Scenarios
-----------

Common test scenarios that should be covered:

1. **Authentication and Authorization**
   * Authentication success/failure
   * Permission checks for all roles
   * Access control to protected resources

2. **Data Validation**
   * Required fields validation
   * Data type and format validation
   * Business rule validation
   * Edge case handling

3. **Business Logic**
   * Booking creation and management
   * Package purchase and redemption
   * Payment processing
   * Schedule management

4. **Error Handling**
   * Database errors
   * External service failures
   * Input validation errors
   * Resource conflicts

5. **User Flows**
   * Registration and onboarding
   * Booking an appointment
   * Managing user profile
   * Instructor availability management

Testing Best Practices
--------------------

1. **Write Tests First**: Consider test-driven development (TDD) for complex features
2. **Keep Tests Fast**: Optimize for quick execution to enable rapid feedback
3. **One Assertion per Test**: Focus each test on a single behavior
4. **Use Setup and Teardown**: Properly manage test state
5. **Avoid Test Interdependence**: Tests should be able to run in any order
6. **Clean Test Code**: Apply the same quality standards to test code as production code
7. **Mock External Dependencies**: Isolate tests from external services
8. **Test Both Positive and Negative Cases**: Cover success and failure scenarios
