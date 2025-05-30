from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div
from django_countries.fields import CountryField

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'given-name'})
    )
    last_name = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'family-name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'autocomplete': 'street-address'
        }),
        required=True
    )
    city = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'address-level2'})
    )
    postal_code = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'postal-code'})
    )
    country = CountryField().formfield(
        required=True,
        widget=forms.Select(attrs={'autocomplete': 'country'})
    )
    stripe_token = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_id = 'checkout-form'
        self.helper.add_input(Submit('submit', 'Place Order', css_class='btn-primary'))