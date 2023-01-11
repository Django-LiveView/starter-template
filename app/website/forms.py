from django import forms
from app.website.models import Cat
from django.utils.translation import gettext as _
from django.core import validators
from django.core.exceptions import ValidationError


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

    def save(self):
        return Cat.objects.create(
            name=self.cleaned_data["name"],
            age=self.cleaned_data["age"],
            biography=self.cleaned_data["biography"],
            avatar=self.cleaned_data["avatar"],
        )


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
            }
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
        label=_("Mesaage"),
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
