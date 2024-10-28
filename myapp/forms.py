from django import forms
from .models import Client

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'adresse', 'télé', 'age', 'sexe', 'email']