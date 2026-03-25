# Generated migration for critical database constraints
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_remove_booking_package'),  # Update with your latest migration
    ]

    operations = [
        # Add unique constraint to prevent double bookings
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.UniqueConstraint(
                fields=['instructor', 'start_time', 'end_time'],
                condition=models.Q(status__in=['confirmed', 'in_progress']),
                name='unique_active_booking_per_instructor_time',
            ),
        ),
        # Add unique constraint on transaction_id (when not blank)
        migrations.AddConstraint(
            model_name='bookingpayment',
            constraint=models.UniqueConstraint(
                fields=['transaction_id'],
                condition=models.Q(transaction_id__gt=''),
                name='unique_transaction_id',
            ),
        ),
        # Add check constraint: end_time > start_time
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(
                check=models.Q(end_time__gt=models.F('start_time')),
                name='end_time_after_start_time',
            ),
        ),
        # Add check constraint: total_price >= 0
        migrations.AddConstraint(
            model_name='booking',
            constraint=models.CheckConstraint(
                check=models.Q(total_price__gte=0),
                name='total_price_non_negative',
            ),
        ),
        # Add check constraint: amount >= 0 for payments
        migrations.AddConstraint(
            model_name='bookingpayment',
            constraint=models.CheckConstraint(
                check=models.Q(amount__gte=0),
                name='payment_amount_non_negative',
            ),
        ),
    ]

