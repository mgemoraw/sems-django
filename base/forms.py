from django import forms

from api.models import Department, User
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']

        widgets = {
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room name...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write something about this room...',
                'rows': 4
            }),
        }

class UserRegisterForm(forms.ModelForm):
    # Using ModelChoiceField to pull from your Department model
    # department = forms.ModelChoiceField(
    #     queryset=Department.objects.all(),
    #     empty_label="Select Department",
    #     widget=forms.Select(attrs={
    #         'class': 'auth-input',
    #     })
    # )
    class Meta:
        model = User  # Changed from Room to User
        fields = ['username', 'first_name', 'last_name', 'email', "department", 'password']
        
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Enter username...'
    }))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Enter first name...'
    }))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Enter last name...'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Enter email...'
    }))
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),  
        empty_label="Select Department",
        widget=forms.Select(attrs={
            'class': 'auth-input',
        })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Enter password...'
    }))



    # This method ensures the password is encrypted correctly in the database
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user