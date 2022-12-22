from django.contrib.auth.models import User
from app.website.models import Profile
from faker import Faker
from random import randint
import requests
import time
from django.core.files import File
from tempfile import NamedTemporaryFile


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

        # Create profile
        profile = Profile(user=user)
        profile.save()

        # Add profile picture
        url_random_imagen = f"https://cdn.jsdelivr.net/gh/tanrax/place-image-random/images/{randint(1, 1000)}.jpg"
        r = requests.get(url_random_imagen)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        profile.avatar.save(f"random_{int(time.time() * 1000)}.jpg", File(img_temp))

        
        return user

    # Create users
    for _ in range(10):
        create_user()
