from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .forms import ProfileForm, RatingForm
import pyrebase
import datetime
import ast
import string
import random
from . import Checksum

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


def home(request):
    all_list = database.child('Vendors').get().each()
    vendors = {}
    for i in all_list:
        vendors.update({i.key(): i.val()})
    ven_list = {}
    for i in vendors:
        cur = vendors[i]
        addr = cur['address']
        ctime = cur['closingTime']
        email = cur['email']
        name = cur['name']
        otime = cur['openingTime']
        phone = cur['phone']
        _type = cur['type']
        avgprice = cur['avgPrice']
        time = str(otime) + ":00 - " + str(ctime) + ":00"
        d = dict({'Address': addr, 'Time': time, 'Email': email, 'phone': phone,
                  'Type': _type, 'Price': avgprice})
        ven_list.update({name: d})
    return render(request, 'Customer/custhome.html', {'ven_list': ven_list})


def rest_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    restname = request.POST.get('restaurant')
    main = {}
    dessert = {}
    bev = {}

    vendors = data['Vendors']
    for i in vendors:
        if vendors[i]['name'] == restname:
            uid = i
            break
    menu = data['Menus']
    if uid in menu:
        restmenu = menu[uid]
        review = {}
        allreviews = data['Reviews']
        s = 0
        for i in allreviews:
            if allreviews[i]['vendor'] == uid:
                review.update({s: {allreviews[i]['review']: allreviews[i]['rating']}})
                s = s + 1

        return render(request, 'Customer/restaurant_view.html',
                      {'menu': restmenu, "uid": uid, 'reviews': review, 'restname': restname})
    else:
        return redirect('Customer:home')


def profile_view(request):
    all_list = database.child('Users').get().each()
    users = {}
    for i in all_list:
        users.update({i.key(): i.val()})
    for i in users:
        curuser = users[i]
        if curuser['email'] == request.user.email:
            uid = i
            curaddress = curuser['deliveryAddress'].split(',')[0:-1]
            curcity = curuser['deliveryAddress'].split(',')[-1]
            curaddress = ','.join(curaddress)
            curphone = curuser['phone']
            break
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            first_name = request.user.first_name
            last_name = request.user.last_name
            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            phone_number = form.cleaned_data.get('phone_number')
            name = first_name + " " + last_name
            addressfull = address + "," + city
            newdata = {"deliveryAddress": addressfull, "email": request.user.email, "name": name, "phone": phone_number}
            database.child("Users").child(uid).update(newdata)
            return redirect('Customer:home')
    else:
        form = ProfileForm(initial={"address": curaddress, 'city': curcity, "phone_number": curphone})
    return render(request, 'Customer/profile.html', {'form': form})


@csrf_exempt
def cart_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})
    restid = request.POST.get('restaurant')
    order = {}
    total = 0
    restmenu = data['Menus'][restid]
    for j in restmenu:
        for i in restmenu[j]:
            item = restmenu[j][i]
            quantity = request.POST.get(i)
            quantity = int(quantity)
            if quantity > 0:
                price = item['price']
                price = int(price)
                item = dict({"quantity": quantity, "price": price})
                order.update({i: item})
                total = total + price * quantity
    transaction = dict({"order": order, "restid": restid, "total": total})
    return render(request, 'Customer/cart.html', {"order": order, "restid": restid, "total": total,
                                                  "restname": data['Vendors'][restid]['name']})


def assignDeliverer():
    all_list = database.child('Deliverers').get().each()
    deliverers = {}
    for i in all_list:
        deliverers.update({i.key(): i.val()})
    for i in deliverers:
        if deliverers[i]['isFree'] == "Yes":
            database.child('Deliverers').child(i).update({'isFree': "No"})
            return deliverers[i]['name'], i

    return "No", "No"


@csrf_exempt
@login_required
def transaction(request, transactiondict):
    mid = 'gqHkIh40947005643657'
    mkey = b'j1_MwAdMph_7xW0I'
    orderID = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    channelid = 'WEB'
    customers = database.child('Users').shallow().get().val()
    curr_customer_list = [i for i in customers if database.child('Users').child(i).child('email').get().val() == request.user.email]
    if curr_customer_list:
        curr_customer = curr_customer_list[0]
    else:
        error_msg = {'msg': "You are not a registered Customer!"}
        return render(request, 'Authentication/login_page.html', error_msg)
    custID = curr_customer

    mobileNo = database.child('Users').child(custID).child('phone').get().val()
    email = request.user.email
    txnAmount = request.GET.get('total')
    website = 'WEBSTAGING'
    industryTypeID = 'Retail'

    context = {
        'MID': mid,
        'ORDER_ID': orderID,
        'CHANNEL_ID': channelid,
        'CUST_ID': custID,
        'MOBILE_NO': mobileNo,
        'EMAIL': email,
        'TXN_AMOUNT': txnAmount,
        'WEBSITE': website,
        'INDUSTRY_TYPE_ID': industryTypeID,
    }
    paytmParams = context
    paytmParams['CALLBACK_URL'] = 'https://mealsonwheels.pythonanywhere.com/customer/post_transaction'
    check_sum_hash = Checksum.generate_checksum(paytmParams, mkey)
    request.session['check_sum_hash'] = check_sum_hash
    temp = {'context': context, 'CHECKSUMHASH': check_sum_hash}

    database.child('Transactions').child('notDelivered').child(orderID).set(transactiondict)
    return render(request, 'Customer/transaction.html', temp)


@csrf_exempt
def post_transaction(request):
    if request.user.is_authenticated:
        return redirect('Authentication:home')
    if request.method == 'POST':
        if request.POST.get('STATUS') != 'TXN_SUCCESS':
            database.child('Transactions').child('notDelivered').child(request.POST.get('ORDERID')).remove()
    return redirect('Customer:home')


@csrf_exempt
def post_cart(request):
    now = datetime.datetime.now()
    itemsOrdered = ast.literal_eval(request.GET.get('order'))
    vendor = request.GET.get('restid')
    vendorName = request.GET.get('restname')
    totalAmount = request.GET.get('total')
    paymentMode = request.GET.get('transaction')
    date = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    customerLocation = request.GET.get('pinlatitude') + "," + request.GET.get('pinlongitude')
    transactionId = "cash"

    delivererName, deliverer = assignDeliverer()
    all_list = database.child('Users').get().each()
    users = {}
    for i in all_list:
        users.update({i.key(): i.val()})
    for i in users:
        if users[i]['email'] == request.user.email:
            customer = i
    transactiondict = {'customer': customer, 'customerLocation': customerLocation, 'date': date,
                       'deliverer': deliverer, 'delivererLocation': ",", 'delivererName': delivererName,
                       'itemsOrdered': itemsOrdered, 'paymentMode': paymentMode, 'totalAmount': totalAmount,
                       'transactionId': transactionId, 'vendor': vendor, 'status': "Cooking", 'vendorName': vendorName}

    if deliverer == "No":
        print('No deliverer is free!')
        return redirect('Customer:home')

    if request.GET.get('transaction') == "paytm":
        return transaction(request, transactiondict)

    database.child('Transactions').child('notDelivered').push(transactiondict)
    return redirect('Customer:home')


def current_orders(request):
    user_list = database.child('Users').get().each()
    all_list = database.child('Transactions').child('notDelivered').get().each()
    orders = {}
    users = {}
    for i in user_list:
        users.update({i.key(): i.val()})
    for i in all_list:
        data = i.val()
        if users[data['customer']]['email'] == request.user.email:
            orders.update({i.key(): i.val()})
    return render(request, 'Customer/current_orders.html', {'orders': orders})


def order(request):
    uid = request.POST.get('restaurant')
    all_list = database.child('Transactions').child('notDelivered').child(uid).get().each()
    order = {}
    for i in all_list:
        order.update({i.key(): i.val()})
    return render(request, 'Customer/order.html', {'order': order, 'uid': uid})


def dashboard_view(request):
    all_list = database.get().each()
    data = {}
    for i in all_list:
        data.update({i.key(): i.val()})

    users = data['Users']
    all_reviews = data['Reviews']
    for i in users:
        cur_user = users[i]
        if cur_user['email'] == request.user.email:
            uid = i
            break
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            vendor = form.cleaned_data.get('vendor')
            rating = form.cleaned_data.get('rating')
            review = form.cleaned_data.get('review')
            id = form.cleaned_data.get('id')
            customer = form.cleaned_data.get('customer')
            curr_rating = float(data['Vendors'][vendor]['rating'])
            noOfRatings = int(data['Vendors'][vendor]['noOfRatings'])
            curr_rating = (curr_rating * noOfRatings + int(rating)) / (noOfRatings + 1)
            noOfRatings = noOfRatings + 1
            database.child('Vendors').child(vendor).child('rating').set(str(curr_rating))
            database.child('Vendors').child(vendor).child('noOfRatings').set(str(noOfRatings))
            newdata = {'customer': customer, 'rating': rating, 'review': review, 'vendor': vendor}

            database.child("Reviews").child(id).set(newdata)
            return redirect('Customer:dashboard')

    del_trans = data['Transactions']['delivered']

    trans = {}
    for j in del_trans:
        if j is not None:
            if del_trans[j]['customer'] == uid:
                date = del_trans[j]['date']
                itemsOrdered = del_trans[j]['itemsOrdered']
                customer = del_trans[j]['customer']
                paymentMode = del_trans[j]['paymentMode']
                totalAmount = del_trans[j]['totalAmount']
                vendor = del_trans[j]['vendor']
                vendor_name = data['Vendors'][vendor]['name']
                if j in all_reviews.keys():
                    curr_rating = float(all_reviews[j]['rating'])
                    curr_review = all_reviews[j]['review']
                else:
                    curr_rating = 0
                    curr_review = "Write your review"
                c = {'id': j, 'date': date, 'itemsOrdered': itemsOrdered, 'paymentMode': paymentMode,
                     'totalAmount': totalAmount, 'vendor': vendor, 'vendorname': vendor_name,
                     'customer': customer, 'rating': curr_rating, 'review': curr_review}
                trans.update({j: c})
    return render(request, 'Customer/dashboard.html', {'trans': trans})
