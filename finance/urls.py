from django.urls import path 
from .import views 

urlpatterns = [
    path("Invoices",views.Invoices,name="Invoices"),
    path("Incomes",views.Incomes,name="Incomes"),
    path("Expenses",views.Expenses,name="Expenses"),
    path("Finance_settings",views.Finance_settings,name="Finance_settings"),
    path("add_price_slab",views.add_price_slab,name="add_price_slab"),
    path("generete_invoice/<int:pk>",views.generete_invoice,name="generete_invoice"),
    path("get_invoice/<int:pk>",views.get_invoice,name="get_invoice")

]