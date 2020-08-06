from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(ProfileForm, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']
    address = forms.CharField(max_length=250, required=True)
    city = forms.CharField(max_length=250, required=True, help_text='State assumed to be Assam')
    phone_number = forms.RegexField(regex=r'^\d{10}$',required=True,help_text="Phone number must be 10 digits.(+91 not required)")

    class Meta:
        model = User
        fields = ('address','city','phone_number')

class RatingForm(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(RatingForm, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']
    vendor = forms.CharField(max_length=200)
    id = forms.CharField(max_length=100)
    rating = forms.CharField(max_length=1)
    review = forms.CharField(max_length=100)
    customer = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('vendor','review', 'rating', 'id', 'customer')