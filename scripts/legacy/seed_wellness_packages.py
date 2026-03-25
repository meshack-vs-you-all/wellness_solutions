import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from services.models import Service, ServicePackage

def seed_packages():
    print("🛒 Seeding Wellness Packages...")
    service = Service.objects.filter(name="Full Body Stretch").first()
    if not service:
        print("❌ Service not found. Run seed_demo_users.py first.")
        return

    packages = [
        {
            "name": "5-Session Recovery Pack",
            "sessions": 5,
            "discount": 10.00, # 10%
        },
        {
            "name": "10-Session Performance Pack",
            "sessions": 10,
            "discount": 20.00, # 20%
        },
        {
            "name": "Unlimited Monthly Membership",
            "sessions": 30,
            "discount": 50.00, # 50%
        }
    ]

    for p in packages:
        pkg, created = ServicePackage.objects.get_or_create(
            name=p["name"],
            defaults={
                "service": service,
                "sessions": p["sessions"],
                "discount_percentage": Decimal(str(p["discount"])),
                "price_per_session": service.price * (1 - Decimal(str(p["discount"])) / 100),
                "validity_days": 90
            }
        )
        status = "[CREATED]" if created else "[EXISTS]"
        print(f"{status} {p['name']}")

if __name__ == "__main__":
    seed_packages()
