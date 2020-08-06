from django.urls import path
from . import views

app_name = 'Vendor'

urlpatterns = [
	path('menu/', views.menu, name='menu'),
	path('current_orders/', views.curr_orders, name='curr_orders'),
	path('reviews/', views.reviews, name='reviews'),
	path('post_menu/', views.post_menu, name='post_menu'),
	path('edit_details/', views.edit_details, name='edit_details'),
	path('post_edit_details/', views.post_edit_details, name='post_edit_details'),
]