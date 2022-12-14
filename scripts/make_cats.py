from app.website.models import Cat
from faker import Faker
import shutil

def run():
    Cat.objects.all().delete()
    shutil.rmtree('media/avatars/', ignore_errors=True)
    
    for num in range(1, 11):
        new_cat = Cat()
        new_cat.name = Faker().name()
        new_cat.age = Faker().random_int(min=1, max=15)
        new_cat.biography = Faker().text()
        new_cat.save()
        # Save avatar from image path
        avatar_cat = open(f'static/img/cats/cat-{num}.jpg', 'rb')
        new_cat.avatar.save(f'cat-{num}.jpg', avatar_cat)
        
