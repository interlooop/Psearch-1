from django import forms
from django.core.validators import RegexValidator

from .models import Product



class ShippingAddressForm(forms.Form):
    address=forms.CharField(max_length=200,required=True,help_text="Enter address",
        widget=forms.TextInput(attrs={'placeholder': 'Address','class':'form-control','style':'margin: 5px;','name':'address','autocomplete':'off'}),
        validators=[
            RegexValidator(
                    regex=r'^[a-zA-Z0-9\s\'\-]*$',
                    message='Only alphanumeric characters,- and \' are allowed for the address field.',
                    code='invalid_address_field'
                ),
            ])

    city=forms.CharField(max_length=200,required=True,help_text="Enter city",
        widget=forms.TextInput(attrs={'placeholder': 'City','class':'form-control','style':'margin: 5px;','name':'city','autocomplete':'off'}),
        validators=[
            RegexValidator(
                    regex=r'^[a-zA-Z\s\'\-]*$',
                    message='Only alphabetic characters,- and \' are allowed for the city field.',
                    code='invalid_city_field'
                ),
            ])

    state=forms.CharField(max_length=200,required=True,help_text="Enter state",
        widget=forms.TextInput(attrs={'placeholder': 'State','class':'form-control','style':'margin: 5px;','name':'state','autocomplete':'off'}),
        validators=[
            RegexValidator(
                    regex=r'^[a-zA-Z\s\'\-]*$',
                    message='Only alphabetic characters,- and \' are allowed for the state field.',
                    code='invalid_state_field'
                ),
            ])

    zipcode=forms.CharField(max_length=200,required=True,help_text="Enter zipcode",
        widget=forms.TextInput(attrs={'placeholder': 'Zipcode','class':'form-control','style':'margin: 5px;','name':'zipcode','autocomplete':'off'}),
        validators=[
            RegexValidator(
                    regex=r'^[a-zA-Z0-9\s\'\-]*$',
                    message='Only alphanumeric characters,- and \' are allowed for the zipcode field.',
                    code='invalid_zipcode_field'
                ),
            ])