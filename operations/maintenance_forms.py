from django import forms
from django.contrib.auth import get_user_model
from .models import MaintenancePlan


class MaintenancePlanForm(forms.ModelForm):
    class Meta:
        model = MaintenancePlan
        fields = ['asset', 'title', 'instructions', 'interval_days', 'next_due', 'priority', 'assigned_to', 'is_active']
        widgets = {'next_due': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = get_user_model().objects.filter(is_active=True, groups__name='Technician').distinct()
