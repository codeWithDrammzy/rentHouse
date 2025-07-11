from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import*

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

class LandlordForm(forms.ModelForm):
    class Meta:
        model = Landlord  # ✅ Capitalized, matches your model class
        fields = '__all__'

class HouseForm(forms.ModelForm):
    
    class Meta:
        model = House
        fields = '__all__'

class TenantForm(forms.ModelForm):
    
    class Meta:
        model = Tenant
        fields = '__all__'
        exclude = ['payment_amount']

        
        
