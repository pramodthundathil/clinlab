from django.urls import path 
from .import views  
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path("Index",views.Index,name="Index"),
    path("calender",views.calender,name="calender"),
    path('',views.SignIn,name="SignIn"),
    path('SignOut', views.SignOut, name='SignOut'),
    path("Units",views.Unit,name="Units"),
    path("profile",views.profile,name="profile"),
    path("ChangeProfilePic/<int:pk>",views.ChangeProfilePic,name="ChangeProfilePic"),
    path("customers",views.customers,name="customers"),
    path("customer_single/<int:pk>",views.customer_single,name="customer_single"),
    path("UploadLeatterHead",views.UploadLeatterHead,name="UploadLeatterHead")
   
]