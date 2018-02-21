from django import forms
from django.contrib.auth.forms import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import re

from .models import Trainee, Training, AssignedTraining, Assignment, Task


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username:
            raise forms.ValidationError("Username field is required.",
                                        code='invalid')
        else:
            return username

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password field is required.",
                                        code='invalid')
        else:
            return password


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Trainee
        fields = [
            'designation'
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['designation'].required=False

    def save(self, *args, **kwargs):
        profile = super(ProfileForm, self).save(commit=False)
        profile.user = kwargs['user']
        profile.save()
        return profile

    def clean_designation(self):
        designation = self.cleaned_data.get("designation")
        if not designation:
            raise forms.ValidationError("Designation field is required.",                                      code='invalid')
        else:
            return designation


class UserForm(forms.ModelForm):

    class Meta:

        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
        # error_messages = {
        #     'password': {
        #        'required': _("This writer's password required.")}
        # }

    # def validate_even(self, value):
    #     if value:
    #         raise ValidationError(
    #             _('%(value)s is not an even number'),
    #             params={'value': value},
    #         )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required=True
        self.fields['last_name'].required=True
        self.fields['email'].required=True
        #self.fields['username'].validators=[self.validate_even]
        self.fields['username'].help_text = ""
        #self.fields['username'].error_messages = {'required': 'Username field is required.'}
        self.fields['password'].required=True

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        if not re.match(r'^[A-Za-z ]+$', first_name):
            raise forms.ValidationError("Special characters or numbers are not valid.",
                                        code = 'invalid')
        else:
            return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name")
        if not re.match(r'^[A-Za-z ]+$', last_name):
            raise forms.ValidationError("Special characters or numbers are not valid.",
                                        code = 'invalid')
        else:
            return last_name

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Password field is required.",
                                        code='invalid')
        else:
            return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email ID field is required.",
                                        code='invalid')
        else:
            return email


class AddTrainingForm(forms.ModelForm):

    class Meta:

        model = Training
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'due_date': forms.TextInput(attrs={'type':'date', 'class':'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AddTrainingForm, self).__init__(*args, **kwargs)
        self.fields['document'].required=False

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if not due_date:
            raise forms.ValidationError("Due date field is required.",
                                        code='invalid')
        else:
            return due_date

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Title field is required.",
                                        code='invalid')
        else:
            return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            raise forms.ValidationError("Description field is required.",
                                        code='invalid')
        else:
            return description


class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            'title',
            'description'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
        }


    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Title field is required.",
                                        code='invalid')
        else:
            return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            raise forms.ValidationError("Description field is required.",
                                        code='invalid')
        else:
            return description



class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = [
            'title',
            'description',
            'assignment_file_path',
            'due_date'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'due_date': forms.TextInput(attrs={'type':'date', 'class':'form-control'}),
            'assignment_file_path': forms.FileInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['assignment_file_path'].required=False


    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if not due_date:
            raise forms.ValidationError("Due date field is required.",
                                        code='invalid')
        else:
            return due_date

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if not title:
            raise forms.ValidationError("Title field is required.",
                                        code='invalid')
        else:
            return title

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if not description:
            raise forms.ValidationError("Description field is required.",
                                        code='invalid')
        else:
            return description