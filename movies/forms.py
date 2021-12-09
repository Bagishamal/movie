import datetime

from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import *


class TextName(forms.Form):
    your_name = forms.CharField(
        label="Твое имя",
        help_text="Attention!",
        initial=datetime.date.today,
        max_length=100,
        widget=forms.Textarea,
        required=False,
        error_messages={"required": "Egghead, what did you do?"}
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ["Text", "Name", "Email"]


class RatingForm(forms.ModelForm):
    Stars = forms.ModelChoiceField(
        widget=forms.RadioSelect(),
        queryset=RatingStars.objects.all(),
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("Stars",)


#
#
# class TestReview(forms.ModelForm):
#     class Meta:
#         model = Reviews
#         fields = ["Name", "Email", "Text"]
#         widgets = {
#             "Text": forms.Textarea(attrs={"cols": 15, "rows": 15})
#         }


# class Comment(forms.ModelForm):
#     # slug = CharField(validators=[validate_Age])
#     class Meta:
#         model = DirectorsActors
#         fields = ["Name", "Age", "Description", "Image"]
# widgets = {
#     "Name": forms.Textarea(attrs={"cols": 10, "rows": 10}),
# }
# labels = {
#     "Name":_("Имя быстро"),
#     "Age":_("Возраст какой а?"),
# }
#
# help_texts={
#     "Name": _("Имя нужно в латинице")
# }

#
# def clean_name(self):
#     name = self.cleaned_data["Name"]
#     if len(name)>6:
#         raise ValidationError("Ты шо правила не читал?")
#     return name


class TestCaptchaForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        help_text="Egghead!",
        max_length=50,
        required=True,
        error_messages={"required": "Egghead, what did you do?"}
    )
    comment = forms.CharField(
        label="Ваш комментарии",
        widget=forms.Textarea(attrs={"cols": '10', "rows": '20'}),
        required=True,
    )
    # captcha = CaptchaField()
    captcha = ReCaptchaField()