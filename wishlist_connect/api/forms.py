from django import forms
from .models import Gift, UserProfile

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['title', 'description', 'price', 'priority']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['visible']