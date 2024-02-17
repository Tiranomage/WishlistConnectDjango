from django import forms
from .models import Gift, UserProfile, GiftType, GiftStatus, GiftPriority, GiftPrice

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ['title', 'description', 'price', 'priority', 'status', 'types', 'image']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['visible']

class GiftFilterForm(forms.Form):
    types = forms.ModelMultipleChoiceField(queryset=GiftType.objects.all(), required=False)
    statuses = forms.ModelMultipleChoiceField(queryset=GiftStatus.objects.all(), required=False)
    necessities = forms.ModelMultipleChoiceField(queryset=GiftPriority.objects.all(), required=False)
    price_min = forms.DecimalField(required=False)
    price_max = forms.DecimalField(required=False)