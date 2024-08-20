from django.urls import path 
from .import views 

urlpatterns = [
    path("Invoices",views.Invoices,name="Invoices"),
    path("Incomes",views.Incomes,name="Incomes"),
    path("Expenses",views.Expenses,name="Expenses"),
    path("Finance_settings",views.Finance_settings,name="Finance_settings"),
    path("add_price_slab",views.add_price_slab,name="add_price_slab"),
    path("generete_invoice/<int:pk>",views.generete_invoice,name="generete_invoice"),
    path("get_invoice/<int:pk>",views.get_invoice,name="get_invoice"),
    path("addprice_ajax",views.addprice_ajax,name="addprice_ajax"),
    path("adjustment/<int:pk>",views.adjustment,name="adjustment"),
    path("delete_invoice/<int:pk>",views.delete_invoice,name="delete_invoice"),
    path("delete_income/<int:pk>",views.delete_income,name="delete_income"),
    path("delete_expence/<int:pk>",views.delete_expence,name="delete_expence"),

]