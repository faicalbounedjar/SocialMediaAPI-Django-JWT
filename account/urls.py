from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/',views.register,name='register'), 
    path('userinfo/', views.current_user,name='user_info'), 
    path('userinfo/update', views.update_user,name='user_update'), 
]
