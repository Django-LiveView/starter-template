from django import forms
from channels.db import database_sync_to_async
from app.website.models import Cat
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.core.exceptions import ValidationError
from app.website.actions.cat_single import get_cat_from_slug


# Custom validators
# https://docs.djangoproject.com/en/4.1/ref/validators/


def validate_checkbox_selected(value):
    if value is False:
        raise ValidationError(
            message=_("You must agree to the terms and conditions."),
        )


# Forms


class CatForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "data-cats-target": "name",
            },
        ),
    )
    age = forms.IntegerField(
        label=_("Age"),
        widget=forms.NumberInput(
            attrs={
                "data-cats-target": "age",
            },
        ),
    )
    biography = forms.CharField(
        label=_("Biography"),
        widget=forms.Textarea(
            attrs={
                "data-cats-target": "biography",
            },
        ),
    )
    avatar = forms.ImageField(
        label=_("Avatar"),
        allow_empty_file=True,
        widget=forms.FileInput(
            attrs={
                "data-cats-target": "avatar",
            },
        ),
    )

    @database_sync_to_async
    def create_cat(self):
        """Create a new cat."""
        cat = Cat.objects.create(**self.cleaned_data)
        cat.age = self.cleaned_data["age"]
        cat.biography = self.cleaned_data["biography"]
        if self.cleaned_data["avatar"]:
            cat.avatar = self.cleaned_data["avatar"]
        cat.save()
        return cat

    @database_sync_to_async
    def update_cat(self, cat):
        """Update an existing cat."""
        for field, value in self.cleaned_data.items():
            if field in ("name", "age", "biography"):
                setattr(cat, field, value)
        if self.cleaned_data["avatar"]:
            cat.avatar = self.cleaned_data["avatar"]
        cat.save()
        return cat

    async def save(self, slug=None):
        """Save the form. If a slug is provided, update the existing cat."""
        cat = await get_cat_from_slug(slug)
        if cat is None:
            return await self.create_cat()
        else:
            return await self.update_cat(cat)
        return cat


class LoginForm(forms.Form):
    email = forms.CharField(
        label=_("Email"),
        max_length=255,
        validators=[validators.EmailValidator(message=_("Invalid email"))],
        error_messages={"required": _("This field is required.")},
        widget=forms.EmailInput(
            attrs={
                "data-login-target": "email",
                "data-action": "keydown.enter->login#logIn",
                "value": "scottmosley@example.org",
            },
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        max_length=100,
        error_messages={"required": _("This field is required.")},
        widget=forms.PasswordInput(
            attrs={
                "data-login-target": "password",
                "data-action": "keydown.enter->login#logIn",
            }
        ),
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=255,
        error_messages={"required": _("This field is required.")},
        widget=forms.TextInput(
            attrs={
                "data-contact-target": "name",
            }
        ),
    )

    email = forms.CharField(
        label=_("Email"),
        max_length=255,
        validators=[validators.EmailValidator(message=_("Invalid email"))],
        error_messages={"required": _("This field is required.")},
        widget=forms.EmailInput(
            attrs={
                "data-contact-target": "email",
            }
        ),
    )

    message = forms.CharField(
        label=_("Message"),
        max_length=1500,
        error_messages={"required": _("This field is required.")},
        widget=forms.Textarea(
            attrs={
                "data-contact-target": "message",
            }
        ),
    )

    is_accept_terms = forms.BooleanField(
        label=_("I accept all cuddles and caresses"),
        required=False,
        validators=[validate_checkbox_selected],
        error_messages={"required": _("You must accept to continue.")},
        widget=forms.CheckboxInput(
            attrs={
                "data-contact-target": "isAcceptTerms",
                "checked": False,
            }
        ),
    )
