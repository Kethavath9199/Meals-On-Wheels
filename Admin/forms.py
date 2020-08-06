from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class vendorform(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(VendorForm, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']

    address = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=250, required=True, help_text='State assumed to be Assam')
    phone_number = forms.RegexField(regex=r'^\d{10}$', required=True,
                                    help_text="Phone number must be 10 digits.(+91 not required)")
    avgPrice = forms.DecimalField(min_value=0, required=True)
    closingTime = forms.CharField(max_length=250, required=True)
    type = forms.CharField(max_length=250, required=True)
    openingTime = forms.CharField(max_length=250, required=True)

    class Meta:
        model = User
        fields = ('address', 'city', 'phone_number', 'avgPrice', 'avgPrice', 'closingTime', 'type', 'openingTime')


class delivererform(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(delivererform, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']

    address_line1 = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=30, required=True, help_text='State assumed to be Assam')
    phone_number = forms.RegexField(regex=r'^\d{10}$', help_text="Phone number must be 10 digits.(+91 not required)")

    class Meta:
        model = User
        fields = ('address_line1', 'city', 'phone_number')


class adddelivererform(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(adddelivererform, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']

    name = forms.CharField(max_length=250, required=True)
    email = forms.EmailField(required=True)
    address_line1 = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=30, required=True, help_text='State assumed to be Assam')
    phone_number = forms.RegexField(regex=r'^\d{10}$', help_text="Phone number must be 10 digits.(+91 not required)")

    class Meta:
        model = User
        fields = ('name', 'email', 'address_line1', 'city', 'phone_number')
