from django.urls import path, include
from . import views

app_name = 'Authentication'

urlpatterns = [
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_view, name='logout'),
	path('', views.home, name='home'),
	path('signup/', views.signup, name='signup'),
]
