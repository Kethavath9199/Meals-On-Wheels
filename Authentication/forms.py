from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(SignUpForm, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']
    address_line1 = forms.CharField(max_length=250, required=False)
    city = forms.CharField(max_length=30, required=False, help_text='State assumed to be Assam')
    phone_number = forms.RegexField(regex=r'^\d{10}$',help_text="Phone number must be 10 digits.(+91 not required)")

    class Meta:
        model = User
        fields = ('address_line1','city')