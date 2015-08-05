from django import forms
from models import Text, Author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import *
from crispy_forms.bootstrap import *


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label="Your mail address")
    mail_copy = forms.BooleanField(help_text="Check to get a copy of the mail",
                                   required=False)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))



class SearchTextsForm(forms.Form):
    keyword = forms.CharField()


class TextForm(forms.ModelForm):

    class Meta:
        model = Text
        fields = ("title_english", "title_chinese", "author",
                  "content_english", "content_chinese", )

    def __init__(self, *args, **kwargs):
        super(TextForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        self.helper.layout = Layout(
            MultiField(
                '<h1>Add a text:</h1>',
                Div(
                    HTML("""
                        Pick an author in the list, or <a href="{% url "create_author" %}">create one</a>.
                    """),
                    'author',
                ),
                Div(
                    'title_chinese',
                    'content_chinese',
                    css_class="col-sm-6",
                ),
                Div(
                    'title_english',
                    'content_english',
                    css_class="col-sm-6",
                ),
            ),
            FormActions(
                Submit('submit', 'Submit', css_class='button white')
            )
        )


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("name_chinese", "name_pinyin",)

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))


class LoginForm(forms.Form):
    username = forms.CharField(label="User Name", max_length=30)
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))


class UserCreationMailForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", 'email')

    def __init__(self, *args, **kwargs):
        super(UserCreationMailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = ""
        self.helper.add_input(Submit('submit', 'Submit'))
