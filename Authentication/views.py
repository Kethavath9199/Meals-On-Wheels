from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
import pyrebase
import Vendor.views

config = {
    'apiKey': "AIzaSyC6MLEYIZxv7DHhs-vtmCB3rLkd1y2r3bI",
    'authDomain': "mealsonwheelsiit.firebaseapp.com",
    'databaseURL': "https://mealsonwheelsiit.firebaseio.com",
    'projectId': "mealsonwheelsiit",
    'storageBucket': "mealsonwheelsiit.appspot.com",
    'messagingSenderId': "755544742392"
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

all_list = database.get().each()

data = {}

for i in all_list:
    data.update({i.key(): i.val()})


# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('Authentication:home')
    return render(request, 'Authentication/login_page.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('Authentication:login')
    return redirect('Authentication:login')


def home(request):
    all_list = database.get().each()

    data = {}

    for i in all_list:
        data.update({i.key(): i.val()})
    if request.user.is_authenticated:
        if request.user.email == "mealsonwheelsiitg@gmail.com":
            return redirect('Admin:home')
        customers = data['Users']
        for i in customers:
            curemail = customers[i]['email']
            if curemail == request.user.email:
                return redirect('Customer:home')

        vendors = data['Vendors']
        for i in vendors:
            curemail = vendors[i]['email']
            if curemail == request.user.email:
                return Vendor.views.home(request, i)

        delivery = data['Deliverers']
        for i in delivery:
            curemail = delivery[i]['email']
            if curemail == request.user.email:
                return render(request, 'Authentication/home.html', {'usertype': 'Delivery'})

        return redirect('Authentication:signup')
    else:
        return redirect('Authentication:login')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = request.user.first_name
            last_name = request.user.last_name
            address_line1 = form.cleaned_data.get('address_line1')
            city = form.cleaned_data.get('city')
            phone_number = form.cleaned_data.get('phone_number')
            address = address_line1 + "," + city
            name = first_name + " " + last_name
            newdata = {"deliveryAddress": address, "email": request.user.email, "name": name, "phone": phone_number}
            database.child("Users").push(newdata)
            return redirect('Authentication:home')
    else:
        form = SignUpForm()
    return render(request, 'Authentication/signup.html', {'form': form})
