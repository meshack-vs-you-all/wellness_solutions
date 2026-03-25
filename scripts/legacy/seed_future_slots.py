import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from schedules.models import Schedule, TimeSlot
from wellness_instructors.models import WellnessInstructor

def seed():
    print("Seeding future time slots for ALL instructors...")
    instructors = WellnessInstructor.objects.all()
    if not instructors.exists():
        print("No instructors found.")
        return

    for inst in instructors:
        # Create a schedule for each instructor
        schedule, _ = Schedule.objects.get_or_create(
            instructor=inst,
            weekday=timezone.now().weekday(), # Today
            defaults={
                "start_time": "09:00",
                "end_time": "17:00",
                "is_active": True
            }
        )
        
        # Create slots for the next 5 days
        for day_offset in range(6):
            target_date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)
            
            # Different hours for variety
            hours = [9, 10, 11, 13, 14, 15, 16] if inst.user.email == "steve@jpf.com" else [10, 14]
            
            for hour in hours:
                start = target_date.replace(hour=hour)
                end = start + timedelta(hours=1)
                
                if start < timezone.now():
                    continue
                    
                TimeSlot.objects.get_or_create(
                    schedule=schedule,
                    start_datetime=start,
                    end_datetime=end,
                    defaults={"status": "available"}
                )
    print(f"Done seeding slots for {instructors.count()} instructors.")

if __name__ == "__main__":
    seed()
