Deployment Guide
===============

This document outlines the deployment process for the Wellness Solutions application. It covers development, staging, and production environments, as well as the CI/CD pipeline and infrastructure management.

Deployment Environments
---------------------

The Wellness Solutions platform uses three deployment environments:

1. **Development Environment**
   * Purpose: Active development and testing
   * Access: Developers and internal testers
   * Data: Test data only
   * URL: `dev.jpfstretch.com`

2. **Staging Environment**
   * Purpose: Pre-production testing and client demos
   * Access: Project managers, QA team, and clients for UAT
   * Data: Anonymized production data
   * URL: `staging.jpfstretch.com`

3. **Production Environment**
   * Purpose: Live application for end users
   * Access: End users and system administrators
   * Data: Real production data
   * URL: `app.jpfstretch.com`

Infrastructure Setup
------------------

Cloud Provider
~~~~~~~~~~~~

The Wellness Solutions application is deployed on AWS (Amazon Web Services):

* **EC2 Instances**: Application servers
* **RDS**: PostgreSQL database
* **ElastiCache**: Redis for caching and Celery broker
* **S3**: Static and media file storage
* **CloudFront**: CDN for static assets
* **Route 53**: DNS management
* **VPC**: Network isolation and security
* **ELB**: Load balancing and SSL termination

Infrastructure Architecture
~~~~~~~~~~~~~~~~~~~~~~~~

The infrastructure is organized as follows:

.. code-block:: text

    ┌─────────────┐
    │ CloudFront  │
    │     CDN     │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │    Load     │
    │  Balancer   │
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
┌─────────┐  ┌─────────┐
│   App   │  │   App   │
│ Server 1│  │ Server 2│
└────┬────┘  └────┬────┘
     │            │
     └────┬───────┘
          │
    ┌─────▼──────┐
    │ PostgreSQL │
    │  Database  │
    └─────┬──────┘
          │
    ┌─────▼──────┐
    │   Redis    │
    │   Cache    │
    └────────────┘

Containerization
~~~~~~~~~~~~~~

The application is containerized using Docker:

* **Web Application**: Django application
* **Celery Workers**: Background task processing
* **Celery Beat**: Scheduled tasks
* **Nginx**: Static file serving and proxy

Docker Compose is used for local development, while Kubernetes is used for orchestration in staging and production environments.

CI/CD Pipeline
-----------

Continuous Integration
~~~~~~~~~~~~~~~~~~~

We use GitHub Actions for continuous integration:

1. Code is pushed to a feature branch
2. GitHub Actions runs:
   * Code linting
   * Unit tests
   * Integration tests
   * Code coverage analysis
3. Pull request is created for code review
4. Automated checks must pass before merging

Continuous Deployment
~~~~~~~~~~~~~~~~~~

Automated deployment process:

1. **Development Environment**:
   * Auto-deploys on merge to `develop` branch
   * Deployment takes approximately 5-10 minutes

2. **Staging Environment**:
   * Auto-deploys on merge to `release/*` branches
   * Requires approval from QA team
   * Deployment takes approximately 10-15 minutes

3. **Production Environment**:
   * Auto-deploys on merge to `main` branch
   * Requires approval from project manager
   * Deployment takes approximately 15-20 minutes
   * Includes database backup before deployment

Deployment Workflow
~~~~~~~~~~~~~~~~

Our deployment process follows these steps:

1. **Build Phase**:
   * Create Docker images for each service
   * Tag images with Git commit SHA
   * Push images to container registry

2. **Test Phase**:
   * Run tests against the built images
   * Verify application health checks
   * Validate environment configurations

3. **Deploy Phase**:
   * Update Kubernetes manifests
   * Apply database migrations
   * Roll out new containers
   * Verify deployment success

4. **Post-Deploy Phase**:
   * Run smoke tests
   * Monitor application metrics
   * Update documentation if needed

Database Migrations
-----------------

Managing database schema changes:

1. **Create Migrations**:
   * Run `python manage.py makemigrations` locally
   * Commit migration files to version control

2. **Apply Migrations**:
   * Migrations are automatically applied during deployment
   * Run with `python manage.py migrate`
   * Zero-downtime migrations for production

3. **Migration Best Practices**:
   * Always make migrations backward compatible when possible
   * For large tables, consider batched migrations
   * Test migrations on a copy of production data before deployment

Example migration strategy for large tables:

.. code-block:: python

    # In a custom migration file
    from django.db import migrations, models
    
    def migrate_data_in_batches(apps, schema_editor):
        YourModel = apps.get_model('your_app', 'YourModel')
        db_alias = schema_editor.connection.alias
        
        # Process in batches of 1000
        total = YourModel.objects.using(db_alias).count()
        batch_size = 1000
        
        for i in range(0, total, batch_size):
            batch = YourModel.objects.using(db_alias).all()[i:i+batch_size]
            for item in batch:
                # Perform updates
                item.new_field = transform_data(item.old_field)
                item.save(using=db_alias)
    
    class Migration(migrations.Migration):
        dependencies = [
            ('your_app', '0001_previous_migration'),
        ]
        
        operations = [
            migrations.AddField(
                model_name='yourmodel',
                name='new_field',
                field=models.CharField(max_length=255, null=True),
            ),
            migrations.RunPython(migrate_data_in_batches),
        ]

Environment Variables
------------------

Environment-specific configuration is managed through environment variables:

1. **Local Development**:
   * Stored in `.env` file (not committed to version control)
   * Sample provided in `.env.example`

2. **CI/CD Environments**:
   * Stored in GitHub Secrets for build pipeline
   * Injected during deployment process

3. **Deployment Environments**:
   * Stored in AWS Parameter Store
   * Encrypted sensitive values

Essential environment variables:

.. code-block:: text

    # Database Configuration
    DATABASE_URL=postgres://user:password@host:port/dbname
    
    # Redis Configuration
    REDIS_URL=redis://host:port/db
    
    # Django Settings
    DJANGO_SETTINGS_MODULE=config.settings.production
    DJANGO_SECRET_KEY=your-secret-key
    DJANGO_ALLOWED_HOSTS=app.jpfstretch.com
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID=your-access-key
    AWS_SECRET_ACCESS_KEY=your-secret-key
    AWS_STORAGE_BUCKET_NAME=jpfstretch-media
    
    # Email Configuration
    EMAIL_HOST=smtp.sendgrid.net
    EMAIL_HOST_USER=apikey
    EMAIL_HOST_PASSWORD=your-sendgrid-api-key
    
    # Payment Gateway Configuration
    STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
    STRIPE_SECRET_KEY=your-stripe-secret-key
    
    # Logging
    SENTRY_DSN=your-sentry-dsn

Static and Media Files
--------------------

Static and media file management:

1. **Static Files**:
   * Collected during build phase with `collectstatic`
   * Stored in S3 bucket
   * Served through CloudFront CDN
   * Cache headers set for optimal performance

2. **Media Files**:
   * User-uploaded content stored in S3 bucket
   * Served through CloudFront with signed URLs for private content
   * Virus scanning for uploaded files

S3 bucket configuration:

.. code-block:: bash

    # Create buckets
    aws s3 mb s3://jpfstretch-static
    aws s3 mb s3://jpfstretch-media
    
    # Set bucket policies (example for static bucket)
    aws s3api put-bucket-policy --bucket jpfstretch-static --policy file://static-bucket-policy.json
    
    # Enable versioning
    aws s3api put-bucket-versioning --bucket jpfstretch-media --versioning-configuration Status=Enabled

Scaling and Performance
---------------------

Horizontal Scaling
~~~~~~~~~~~~~~~~

The application scales horizontally:

* Auto-scaling groups for application servers
* Read replicas for database
* Redis cluster for caching

Performance considerations:

* Load testing before major releases
* Performance monitoring with Datadog
* Database query optimization
* CDN for static assets

Cache Strategy
~~~~~~~~~~~~

Multi-level caching strategy:

1. **Browser Cache**:
   * Cache headers for static assets
   * ETag for API responses

2. **CDN Cache**:
   * Static assets cached at edge locations
   * Cache invalidation during deployments

3. **Application Cache**:
   * Django cache framework with Redis backend
   * Cache expensive operations and database queries

Example cache configuration:

.. code-block:: python

    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env('REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'IGNORE_EXCEPTIONS': True,
            }
        }
    }
    
    CACHE_TTL = 60 * 15  # 15 minutes

Monitoring and Logging
--------------------

Application Monitoring
~~~~~~~~~~~~~~~~~~~

We use multiple tools for monitoring:

* **Datadog**: Application performance monitoring
* **Sentry**: Error tracking
* **ELK Stack**: Log aggregation and analysis
* **Prometheus**: Metrics collection
* **Grafana**: Metrics visualization

Key metrics to monitor:

* Response time by endpoint
* Error rates
* Database query performance
* Memory usage
* CPU utilization
* Cache hit/miss rates

Log Management
~~~~~~~~~~~~

Centralized logging with the ELK stack:

* **Elasticsearch**: Log storage and search
* **Logstash**: Log processing pipeline
* **Kibana**: Log visualization and dashboards

Log levels and destinations:

* **DEBUG**: Local development only
* **INFO**: Normal operation events
* **WARNING**: Potential issues that don't affect operation
* **ERROR**: Application errors that require attention
* **CRITICAL**: Severe errors that require immediate action

Example logging configuration:

.. code-block:: python

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/jpfstretch/app.log',
                'maxBytes': 1024 * 1024 * 10,  # 10 MB
                'backupCount': 5,
                'formatter': 'verbose',
            },
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file', 'sentry'],
                'level': 'INFO',
                'propagate': True,
            },
            'wellness_solutions': {
                'handlers': ['console', 'file', 'sentry'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }

Alerting
~~~~~~~

Alert configuration:

* **Critical Alerts**: Paged to on-call engineer
* **Warning Alerts**: Sent to Slack channel
* **Informational Alerts**: Logged for review

Alert thresholds:

* Error rate > 1% of requests
* API response time > 2 seconds
* CPU usage > 80% for 5 minutes
* Memory usage > 85%
* Database connection pool at > 80% capacity

Backup and Disaster Recovery
--------------------------

Backup Strategy
~~~~~~~~~~~~~

Regular backups for all environments:

* **Production Database**:
  * Full backup daily
  * Incremental backups every 6 hours
  * Point-in-time recovery enabled
  * 30-day retention period

* **Media Files**:
  * S3 bucket versioning enabled
  * Cross-region replication for disaster recovery
  * 90-day retention period

Disaster Recovery
~~~~~~~~~~~~~~~

Recovery procedures for different scenarios:

1. **Application Failure**:
   * Kubernetes auto-healing for container failures
   * Manual or automated rollback to previous deployment

2. **Database Failure**:
   * Automated failover to replica
   * Restore from backup if data corruption occurs

3. **Region Failure**:
   * Multi-region architecture
   * Manual failover to secondary region
   * Recovery time objective (RTO): 1 hour
   * Recovery point objective (RPO): 15 minutes

Security Considerations
---------------------

Security practices for deployment:

1. **Network Security**:
   * VPC with private subnets for application and database
   * Security groups with least privilege access
   * VPN for administrative access
   * WAF for public endpoints

2. **Application Security**:
   * Regular security updates
   * Dependency vulnerability scanning
   * HTTPS everywhere with TLS 1.2+
   * CSP headers for browser protection

3. **Data Security**:
   * Encryption at rest for all data stores
   * Encryption in transit for all communications
   * PII data handling according to GDPR requirements
   * Data access audit logging

4. **Access Control**:
   * IAM roles with least privilege
   * MFA for all administrative access
   * Regular access reviews
   * Automated provisioning/deprovisioning

Deployment Checklist
------------------

Pre-Deployment
~~~~~~~~~~~~

* [ ] All tests passing in CI
* [ ] Code reviewed and approved
* [ ] Database migrations tested
* [ ] Performance testing completed
* [ ] Security review completed
* [ ] Documentation updated

Deployment
~~~~~~~~~

* [ ] Database backup created
* [ ] Maintenance page enabled (if needed)
* [ ] Deployment script executed
* [ ] Migrations applied
* [ ] Static files collected and deployed
* [ ] Application servers restarted

Post-Deployment
~~~~~~~~~~~~~

* [ ] Smoke tests executed
* [ ] Application health checks passing
* [ ] Monitoring systems verified
* [ ] Performance metrics reviewed
* [ ] Error logs checked
* [ ] Maintenance page disabled (if used)

Rollback Procedure
----------------

If deployment fails, follow these rollback steps:

1. **Kubernetes-based rollback**:

.. code-block:: bash

    # Roll back to previous deployment
    kubectl rollout undo deployment/jpfstretch-web
    
    # Verify rollback status
    kubectl rollout status deployment/jpfstretch-web

2. **Database rollback** (if migrations cause issues):

.. code-block:: bash

    # Revert to previous migration
    python manage.py migrate your_app 0001_previous_migration
    
    # Or restore from pre-deployment backup for more complex cases

3. **Static files rollback**:

.. code-block:: bash

    # Revert to previous S3 bucket version
    aws s3 sync s3://jpfstretch-static-backup s3://jpfstretch-static

4. **Verify system status** after rollback:

.. code-block:: bash

    # Run health checks
    curl https://app.jpfstretch.com/health/
    
    # Check error logs
    tail -f /var/log/jpfstretch/app.log

Common Deployment Issues
----------------------

Troubleshooting common deployment problems:

1. **Database Migration Failures**:
   * Issue: Migration fails due to data constraints
   * Solution: Review migration file, add data validation, consider batched migration

2. **Static Files Not Updated**:
   * Issue: Browser still shows old static files
   * Solution: Check CDN cache invalidation, verify collectstatic ran correctly

3. **Memory Issues**:
   * Issue: Application crashes with OOM errors
   * Solution: Check memory limits, optimize memory usage, increase container resources

4. **Performance Degradation**:
   * Issue: Slow responses after deployment
   * Solution: Check database queries, review new code for performance issues, check caching

5. **Connection Timeouts**:
   * Issue: Services cannot communicate
   * Solution: Verify network configuration, security groups, and DNS settings
