from django import forms
from .models import Room

class RoomCreateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'room_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter room description'}),
            'room_type': forms.Select(attrs={'class': 'form-select'}),
        }