from django import forms
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
