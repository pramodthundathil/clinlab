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
    path("adjustment_custome/<int:pk>",views.adjustment_custome,name="adjustment_custome"),
    path("delete_invoice/<int:pk>",views.delete_invoice,name="delete_invoice"),
    path("delete_income/<int:pk>",views.delete_income,name="delete_income"),
    path("delete_expence/<int:pk>",views.delete_expence,name="delete_expence"),
    path("CreateInvoice/<int:pk>",views.CreateInvoice,name="CreateInvoice"),
    path("Get_Custome_Invoice/<int:pk>",views.Get_Custome_Invoice,name="Get_Custome_Invoice"),
    path("custome_invoiceprint/<int:pk>",views.custome_invoiceprint,name="custome_invoiceprint"),
    path("Create_Customeamount_items/<int:pk>",views.Create_Customeamount_items,name="Create_Customeamount_items"),
    path("Delete_Items/<int:pk>",views.Delete_Items,name="Delete_Items"),

]