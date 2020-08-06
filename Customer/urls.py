from django.urls import path, include
from . import views

app_name = 'Customer'

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant', views.rest_view, name='restaurant'),
    path('profile', views.profile_view, name='profile'),
    path('cart', views.cart_view, name='cart'),
    path('dashboard', views.dashboard_view, name='dashboard'),
    path('postcart', views.post_cart, name='post_cart'),
    path('currentorders',views.current_orders,name='currentorders'),
    path('order',views.order,name='order'),
    # extras added
    path('transaction', views.transaction, name='transaction'),
    path('post_transaction', views.post_transaction, name='post_transaction'),
]
