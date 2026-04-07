from django import forms
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