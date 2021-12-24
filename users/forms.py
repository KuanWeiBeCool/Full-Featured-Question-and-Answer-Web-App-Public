from django import forms
from django.forms.fields import RegexField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import TextInput

from .models import Profile

class RegisterForm(UserCreationForm):
    username = forms.RegexField(
        label=("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': ("Username may contain only letters, numbers and "
                        "@/./+/-/_ characters.")},
        widget=TextInput(attrs={'class': 'input',
                                'required': 'true',
                                # 'placeholder': 'Username'
        })
    )

    email = forms.EmailField(label=("Email"), widget=forms.EmailInput(attrs={'class': 'input', # form-control
                                  'type': 'email',
                                #   'placeholder': 'Email address',
                                  'required': 'true'
    }))

    password1 = forms.CharField(
        label=("Password"),
        widget=forms.PasswordInput(attrs={'class': 'input', # form-control (for register.html)
                                        'type': 'password',
                                        'required': 'true',
                                        # 'placeholder': 'Password',
                                        

        })
    )
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class': 'input', # form-control (for register.html)
                                        'type': 'password',
                                        'required': 'true',
                                        # 'placeholder': "Confirm Password"
        }),
        help_text=("Enter the same password as above, for verification.")
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")
        if password != confirm_password:
            raise forms.ValidationError("Your passwords didn't match!")


class UserUpdateForm(forms.ModelForm):
    username = username = forms.RegexField(
        label=("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=("30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': ("Username may contain only letters, numbers and "
                        "@/./+/-/_ characters.")},
        widget=TextInput(attrs={'required': 'true'})
    )
    email = forms.EmailField(widget=TextInput(attrs={'required': 'true'}))

    class Meta:
        model = User
        fields = ["username", "email"]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

