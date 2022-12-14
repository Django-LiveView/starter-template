from django.db import models
from django.conf import settings


class Cat(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    biography = models.TextField()
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return settings.DOMAIN_URL + settings.MEDIA_URL + self.avatar.name

    def __str__(self):
        return self.name
