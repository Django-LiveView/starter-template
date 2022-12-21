from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class EmailAuthBackend(BaseBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair, then check
    a username/password pair if email failed
    """

    def authenticate(self, request, username=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


