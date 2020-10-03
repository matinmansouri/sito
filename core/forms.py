from django import forms
from . import models
from captcha.fields import ReCaptchaField
from captcha.fields import ReCaptchaV2Checkbox

class AllauthSignupForm(forms.Form):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(), label=''
    )

    def signup(self, request, user):
        """ This function is required otherwise you will get an ImproperlyConfigured exception """
        pass


class CommentForm(forms.ModelForm):
    name = forms.CharField(
        label="نام :",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:50px"
            }
        ))
    email = forms.EmailField(
        label="ایمیل :",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:50px"
            }
        )
    )
    body = forms.CharField(
        label="متن :",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:50px"
            }
        )
    )
    captcha = ReCaptchaField(
        label="",
        widget=ReCaptchaV2Checkbox()
    )

    class Meta:
        model = models.Comment
        fields = ('name', 'email', 'body')


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label="نام :",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:50px"
            }
        ))
    email = forms.EmailField(
        label="ایمیل :",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:50px"
            }
        )
    )
    body = forms.CharField(
        label="متن :",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:50px"
            }
        )
    )
    captcha = ReCaptchaField(
        label="",
        widget=ReCaptchaV2Checkbox()
    )

    class Meta:
        model = models.Contact
        fields = ('name', 'email', 'body')


class CheckoutForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput())
    lastname = forms.CharField(widget=forms.TextInput())
    street_address = forms.CharField(widget=forms.TextInput())
    apartment_address = forms.CharField(required=False, widget=forms.TextInput())
    zip = forms.CharField(widget=forms.TextInput())
    phonenumber = forms.CharField(widget=forms.TextInput())
