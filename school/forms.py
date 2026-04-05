from django import forms
from django.core.validators import RegexValidator
from .models import AdmissionApplication, Enquiry


phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{7,15}$',
    message="Enter a valid phone number (7–15 digits, may include +, spaces, or dashes)."
)


class AdmissionForm(forms.ModelForm):
    """
    Validated admission application form.
    Field names match the raw <input name="..."> attributes in admissions.html.
    """
    phone = forms.CharField(
        max_length=15,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'placeholder': 'e.g. +91 70326 91555'})
    )

    class Meta:
        model = AdmissionApplication
        fields = ['child_name', 'date_of_birth', 'parent_name', 'email', 'phone', 'program', 'message']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_child_name(self):
        name = self.cleaned_data.get('child_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter the child's full name.")
        return name

    def clean_parent_name(self):
        name = self.cleaned_data.get('parent_name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter the parent/guardian's full name.")
        return name


class EnquiryForm(forms.ModelForm):
    """
    Validated enquiry / contact form.
    Field names match the raw <input name="..."> attributes in contact.html.
    """
    phone = forms.CharField(
        max_length=15,
        validators=[phone_validator],
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        msg = self.cleaned_data.get('message', '').strip()
        if len(msg) < 10:
            raise forms.ValidationError("Please write a more detailed message (at least 10 characters).")
        return msg
