from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            return email
        except models.User.DoesNotExist:
            raise forms.ValidationError("User Does Not Exist")

    def clean_password(self):
        password = self.cleaned_data.get("password")

        return password
