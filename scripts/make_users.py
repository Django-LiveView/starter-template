from django.contrib.auth.models import User
from faker import Faker


def run():
    User.objects.filter(is_staff=False).delete()
    
    # Create user
    def create_user():
        fake = Faker()
        user = User.objects.create_user(
            email=fake.unique.email(),
            username=fake.unique.user_name(),
            password="password",
            first_name=fake.first_name(),
            last_name=fake.last_name(),
        )
        return user

    # Create users
    for _ in range(10):
        create_user()
