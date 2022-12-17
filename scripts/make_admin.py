from django.contrib.auth.models import User


def run():
    # Delete all admin users
    User.objects.all().delete()

    # Create superuser
    User.objects.create_superuser(
        email="admin@admin.com", username="admin", password="admin"
    )
