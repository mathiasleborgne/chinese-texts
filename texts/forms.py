from django import forms
from models import Text


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label="Your mail address")
    mail_copy = forms.BooleanField(help_text="Check to get a copy of the mail",
                                   required=False)


class SearchTextsForm(forms.Form):
    keyword = forms.CharField()


class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        exclude = ('date_release',)


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=30)
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)
