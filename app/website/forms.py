from django import forms
from django.utils.translation import gettext as _
import os
import requests
import threading
from django.core import validators


# Custom validators
# https://docs.djangoproject.com/en/4.1/ref/validators/

# Forms


class LoginForm(forms.Form):
    email = forms.CharField(
        label=_("Email"),
        max_length=255,
        validators=[validators.EmailValidator(message=_("Invalid email"))],
        error_messages={"required": _("This field is required.")},
        widget=forms.EmailInput(attrs={"data-login-target": "email"}),
    )
    password = forms.CharField(
        label=_("Password"),
        max_length=100,
        error_messages={"required": _("This field is required.")},
        widget=forms.PasswordInput(attrs={"data-login-target": "password"}),
    )


class ContactForm(forms.Form):

    name = forms.CharField(
        label=_("Tu nombre y apellidos"),
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "data-contact-target": "name",
                "placeholder": _("Nombre y apellidos"),
                "class": "input--main__input",
            }
        ),
    )

    email = forms.EmailField(
        label=_("Tu correo electrónico"),
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                "id": "email",
                "data-contact-target": "email",
                "placeholder": _("Email"),
                "class": "input--main__input",
            }
        ),
    )

    phone = forms.CharField(
        label=_("Tu teléfono"),
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "phone",
                "data-contact-target": "phone",
                "placeholder": _("Teléfono"),
                "class": "input--main__input",
            }
        ),
    )

    message = forms.CharField(
        label=_("Tu mensaje"),
        max_length=1500,
        required=False,
        widget=forms.Textarea(
            attrs={
                "id": "message",
                "data-contact-target": "message",
                "placeholder": _("Mensaje"),
                "class": "input--main__textarea",
            }
        ),
    )

    is_accept_terms = forms.BooleanField(
        label=_("Acepto los términos y condiciones"),
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                "id": "is_accept_terms",
                "data-contact-target": "isAcceptTerms",
                "checked": False,
                "class": "input--checkbox__input",
            }
        ),
    )
    # Input hidden with hcaptcha_key
    hcaptcha_key = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "hcaptcha_key",
                "data-contact-target": "hcaptchaKey",
                "value": os.environ.get("HCAPTCHA_KEY"),
            }
        ),
    )

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError(_("El nombre es obligatorio"))
        return name

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError(_("El email es obligatorio"))
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and phone == "":
            raise forms.ValidationError(_("El teléfono es obligatorio"))
        return phone

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if message and message == "":
            raise forms.ValidationError(_("El mensaje es obligatorio"))
        return message

    def clean_is_accept_terms(self):
        is_accept_terms = self.cleaned_data.get("is_accept_terms")
        if not is_accept_terms:
            raise forms.ValidationError(_("Debe aceptar los términos y condiciones"))
        return is_accept_terms

    def save(self):
        """
        Send the contact form to the API
        """

        def send_email():
            data = {
                "full_name": self.cleaned_data.get("name"),
                "email": self.cleaned_data.get("email"),
                "phone": self.cleaned_data.get("phone"),
                "message": self.cleaned_data.get("message"),
            }
            response = requests.post(
                os.environ.get("API_DOMAIN") + "v1/contact/", data=data
            )

        # Asynchronous call to the API
        threading.Thread(target=send_email).start()
