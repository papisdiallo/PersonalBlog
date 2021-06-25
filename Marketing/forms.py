from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email Address',
        'type': 'email',
    }), label=False)

    class Meta:
        model = Subscriber
        fields = '__all__'
