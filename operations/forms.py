from django import forms
from django.contrib.auth import get_user_model
from .models import Asset,WorkOrder
class AssetForm(forms.ModelForm):
    class Meta:
        model=Asset
        fields=['code','name','location','description','status','criticality','next_maintenance']
        widgets={'next_maintenance':forms.DateInput(attrs={'type':'date'})}
class WorkOrderForm(forms.ModelForm):
    class Meta:
        model=WorkOrder
        fields=['asset','title','description','priority','assigned_to']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].queryset=get_user_model().objects.filter(is_active=True,groups__name='Technician').distinct()
class ResolutionForm(forms.ModelForm):
    class Meta:
        model=WorkOrder;fields=['resolution_notes']
