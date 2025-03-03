import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from core.models import Event
User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Starting data population...")

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username="admin", email="admin@gmail.com", password='admin@123'
            )
            self.stdout.write(self.style.SUCCESS("admin user created "))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Admin user already exists"))

        users = []
        for i in range(1, 6):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=f"user{i}@gmail.com", password="user@123", role="student")
                users.append(user)
        self.stdout.write(self.style.SUCCESS("✅ 5 Users created"))
        
        for i in range(1, 11):
            event_name = f"event{i}"
            if not Event.objects.filter(event_name=event_name).exists():
                event_date = now() + timedelta(days=random.randint(1, 30))
                LOCATIONS = ["Indore", "Dhamnod", "Ujjain", "Maheshwar"]
                location = random.choice(LOCATIONS)
                Event.objects.create(
                    event_name=event_name,
                    date=event_date,
                    description=f"best ever {event_name}",
                    location=location,
                    expired=False,
                )
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ event{i} Event already exists"))
        self.stdout.write(self.style.SUCCESS("✅ 10 Events created"))
        
        self.stdout.write(self.style.SUCCESS("🎉 Data population complete!"))