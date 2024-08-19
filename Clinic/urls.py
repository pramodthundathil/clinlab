from django.urls import path 
from .import views 

urlpatterns = [
    path("SingleTests",views.SingleTests,name="SingleTests"),
    path('add_test_type/', views.add_test_type, name='add_test_type'),
    path("comprehensive_test",views.comprehensive_test,name="comprehensive_test"),
    path("AddComprehensivetest",views.AddComprehensivetest,name="AddComprehensivetest"),
    path("Comprehensive_single/<int:pk>",views.Comprehensive_single,name="Comprehensive_single"),
    path("delete_comprehensive_test/<int:pk>",views.delete_comprehensive_test,name="delete_comprehensive_test"),
    path("addconprehensivetest_ajax/<int:pk>",views.addconprehensivetest_ajax,name="addconprehensivetest_ajax"),
    path("testdeletefromcomtest/<int:pk><int:tk>",views.testdeletefromcomtest,name="testdeletefromcomtest"),
    
    path("conprehensive_addtest_ajax/<int:pk>",views.conprehensive_addtest_ajax,name="conprehensive_addtest_ajax"),
    path("CreateSample",views.CreateSample,name="CreateSample"),
    path("OrderSingle/<int:pk>",views.OrderSingle,name="OrderSingle"),
    path("OrderSingleFinished/<int:pk>",views.OrderSingleFinished,name="OrderSingleFinished"),
    path("Customer_adding_from_single_order/<int:pk>",views.Customer_adding_from_single_order,name="Customer_adding_from_single_order"),
    path('autocomplete/', views.customer_autocomplete, name='customer_autocomplete'),
    path('pending_samples/', views.pending_samples, name='pending_samples'),
    path('completed_samples/', views.completed_samples, name='completed_samples'),
    path('update-order-patient/<int:pk>/', views.update_order_patient, name='update_order_patient'),
    path('update_order_sample/<int:pk>/', views.update_order_sample, name='update_order_sample'),
    path('update_order_doctor/<int:pk>/', views.update_order_doctor, name='update_order_doctor'),
    path('update_order_hospital/<int:pk>/', views.update_order_hospital, name='update_order_hospital'),
    path('addtest_ajax/<int:pk>/', views.addtest_ajax, name='addtest_ajax'),
    path('addresult_ajax/', views.addresult_ajax, name='addresult_ajax'),
    path('delete_test_result/<int:pk>/', views.delete_test_result, name='delete_test_result'),
    path("addcomment_ajax/",views.addcomment_ajax,name="addcomment_ajax"),
    path("ApproveReport/<int:pk>",views.ApproveReport,name="ApproveReport"),

    path("lab_report/<int:pk>",views.lab_report,name="lab_report"),
    path("labreportdownload<int:pk>",views.labreportdownload,name="labreportdownload"),
    path("lab_report_download<int:pk>",views.lab_report_download,name="lab_report_download"),
    path("RecentlycompletedTests",views.RecentlycompletedTests,name="RecentlycompletedTests"),
    
    
]