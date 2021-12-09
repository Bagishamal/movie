from django import forms
from .models import *
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.EmailInput(attrs={'placeholder': "Введите ваш email..."})
        }
