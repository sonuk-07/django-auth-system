from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Registration form 
    UserCreationForm is extended to handle password validation automatically
    includes password1 and password2 
    built in security checks 
    """

    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'Enter your mail'
        })
    )

    first_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'First Name'
        })
    )

    last_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Last Name'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """
        Customize password fields styling
        """
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class':'form-control',
            'paceholder':'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class':'form-control',
            'paceholder':'Confirm Password'
        })


class CustomAuthenticationForm(AuthenticationForm):
    """
    Login form
    change username field to accept email
    add custom styling
    """
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class':'form-control',
            'placeholder':'Enter your email',
            'autofocus':True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':'form-control',
            'placeholder':'Enter your password'
        })
    )