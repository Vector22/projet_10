from django import forms
from django.utils import html
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """ This class extend the UserCreationForm """

    first_name = forms.CharField(max_length=30, required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False,
                                help_text='Optional.')
    email = forms.EmailField(max_length=254,
                             help_text='Required. Enter a valid email\
                             address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', )

"""
Form field for displaying a submit button.
Useful when you need to have a submit button in the middle of your form.

Usage:

SubmitButtonField(label="", initial=u"Your submit button text")
"""


class SubmitButtonWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        buttonClass = "btn btn-warning"
        customButton = """
        <span class="input-group-btn">
        <button type="submit" name="{}" class="{}">
        <span class="fas fa-search"></span>{}</button>
        </span>
        """.format(html.escape(name), buttonClass, value)
        return customButton


class SubmitButtonField(forms.Field):
    def __init__(self, *args, **kwargs):
        if not kwargs:
            kwargs = {}
        kwargs["widget"] = SubmitButtonWidget

        super(SubmitButtonField, self).__init__(*args, **kwargs)

    def clean(self, value):
        return value


class ResearchForm(forms.Form):
    """ The main page and menu research form """

    search = forms.CharField(max_length=254,
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'input form-control',
                                     'placeholder': 'Recherche'
                                 }))
    button = SubmitButtonField(label="", initial=u" Chercher")

    def clean(self):
        cleaned_data = super(ResearchForm, self).clean()
        search = cleaned_data.get('search')

        if not search:
            raise forms.ValidationError('You have to write something to\
                                        research !')
