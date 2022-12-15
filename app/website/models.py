from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Cat(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    biography = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return settings.DOMAIN_URL + settings.MEDIA_URL + self.avatar.name

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name
