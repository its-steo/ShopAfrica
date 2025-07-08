from django import forms
from .models import Subscriber

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2 rounded-l bg-gray-800 border border-gray-700 text-sm text-white placeholder-gray-400 focus:outline-none',
                'placeholder': 'Your email'
            })
        }
