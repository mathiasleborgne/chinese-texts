from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label="Your mail address")
    mail_copy = forms.BooleanField(help_text="Check to get a copy of the mail",
                                   required=False)
