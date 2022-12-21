from django.contrib.auth.models import User
from faker import Faker


def run():
    # Delete all users
    User.objects.filter(is_staff=False).delete()
    
    # Create user
    def create_user():
        fake = Faker()
        user = User(
            email=fake.unique.email(),
            username=fake.unique.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        user.set_password("password")
        user.save()
        return user

    # Create users
    for _ in range(10):
        create_user()
