
# registration/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import TutorProfile, PupilProfile # Assuming these are defined elsewhere

# Define the common attributes dictionary for consistent styling (Bootstrap's form-control)
FORM_CONTROL_ATTRS = {'class': 'form-control'}


# --- student Registration Form ---

class StudentRegistrationForm(UserCreationForm):
    # Style Custom Fields explicitly
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=FORM_CONTROL_ATTRS)
    )
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs=FORM_CONTROL_ATTRS)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style Inherited Fields (username, passwords)
        inherited_fields = ['username', 'password', 'password2']

        for field_name in inherited_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(FORM_CONTROL_ATTRS)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username", "email", "location"]




class TeacherRegistrationForm(UserCreationForm):
    # Style Custom Fields explicitly
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=FORM_CONTROL_ATTRS)
    )
    school = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs=FORM_CONTROL_ATTRS)
    )
    location = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs=FORM_CONTROL_ATTRS)
    )
    certification = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs=FORM_CONTROL_ATTRS)
    )
    bio = forms.CharField(
        required=False,
        # Apply form-control and set a row height for the Textarea
        widget=forms.Textarea(attrs={**FORM_CONTROL_ATTRS, 'rows': 4})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Style Inherited Fields (username, passwords)
        inherited_fields = ['username', 'password', 'password2']

        for field_name in inherited_fields:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(FORM_CONTROL_ATTRS)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            "username",
            "email",
            "school",
            "location",
            "certification",
            "bio"
        ]
