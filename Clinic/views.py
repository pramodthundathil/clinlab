from django.shortcuts import render, redirect
from .models import TestType, Order, TestResult, ComprehensiveTest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Home.models import Units, Patient, LabDetails
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from datetime import timedelta,  datetime

today = datetime.now()
daybeforeyesterday = today - timedelta(2)


from django import template
from itertools import groupby

register = template.Library()

@register.filter
def groupby(value, arg):
    return groupby(value, key=lambda x: getattr(x, arg))

'''
views is for handling tests and comprehesive tests
this view include

1. Single test view function
2. For Saving the test data with ajax

'''

# Single test view from the dashbord and serves all tests to the function
# also POST method to add new test type 
# model TestType

#1.Single test view function

def SingleTests(request):
    clinicaltest = TestType.objects.all().order_by('-name')
    units = Units.objects.all()
    context = {
        "clinicaltests":clinicaltest,
        "units":units
    }
    return render(request,"pathology/singletests.html",context)

#2. For Saving the test data with ajax


@csrf_exempt
def add_test_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        normal_range = request.POST.get('range')
        Interpertaion_description = request.POST.get('inter_dis')
        unit = request.POST.get('unit')

        try:
            test_type = TestType(
                name=name,
                description=description,
                normal_range=normal_range,
                Interpertaion_description=Interpertaion_description,
                unit=unit
            )
            test_type.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


# comprehensive tests 
def comprehensive_test(request):
    tests = ComprehensiveTest.objects.filter(add_by = request.user) 
    context = {
        "tests":tests
    }
    return render(request,'pathology/comprehensive_tests.html',context)


def AddComprehensivetest(request):
    if request.method == "POST":
        name = request.POST.get('name')
        specimen = request.POST.get('specimen')
        description = request.POST.get('description')
        try:
            test = ComprehensiveTest.objects.create(name = name,specimen = specimen, description = description, add_by = request.user )
            test.save()
        except:
            messages.info(request,"Something worng...")
            return redirect("comprehensive_test")
        return redirect("Comprehensive_single",pk = test.id)
    else:
        return redirect("comprehensive_test")
        

def delete_comprehensive_test(request,pk):
    test = ComprehensiveTest.objects.get(id = pk)
    test.delete()
    messages.info(request, "Test Deleted success....")
    return redirect("comprehensive_test")

def Comprehensive_single(request,pk):
    test = ComprehensiveTest.objects.get(id = pk)
    tests = TestType.objects.all()


    context = {
        'test':test,
        "tests":tests
    }
    return render(request,'pathology/comprehensive_test_add_single.html',context)

@csrf_exempt
def addconprehensivetest_ajax(request,pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        com_test = get_object_or_404(ComprehensiveTest, id=pk)
        testid = request.POST.get('testid')
        test = TestType.objects.get(id = testid)
        
        if test:
            try:
                com_test.tests.add(test)
                com_test.save()
                
                testdeatil_table = render_to_string('ajaxtemplates/comprehensivetable.html', {'results': com_test})
                return JsonResponse({'success': True,"error": "testdeatil_table"})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def testdeletefromcomtest(request,pk,tk):
    ctest = ComprehensiveTest.objects.get(id = pk)
    test = TestType.objects.get(id = tk)
    ctest.tests.remove(test)
    messages.info(request,"One item removed from test..")
    return redirect("Comprehensive_single", pk=pk)


# 3. Order Creation Sample Collection

def CreateSample(request):
    new_order = Order.objects.create(user = request.user )
    new_order.save()
    return redirect(OrderSingle,pk = new_order.id)


def OrderSingle(request,pk):
    new_order = Order.objects.get(id = pk)
    patient = Patient.objects.filter(user = request.user)
    tests = TestType.objects.all()
    c_tests = ComprehensiveTest.objects.all()
    results  = TestResult.objects.filter(order = new_order)
    normal_test = TestResult.objects.filter(order = new_order, is_comprehensive = False)
    com_test = TestResult.objects.filter(order = new_order, is_comprehensive = True )

    context = {
        "new_order":new_order,
        "patient":patient,
        "tests":tests,
        "results":results,
        "c_tests":c_tests
    }
    
    return render(request,"laboratory/addsample.html",context) 

def OrderSingleFinished(request,pk):
    new_order = Order.objects.get(id = pk)
    patient = Patient.objects.filter(user = request.user)
    tests = TestType.objects.all()
    results  = TestResult.objects.filter(order = new_order)
    context = {
        "new_order":new_order,
        "patient":patient,
        "tests":tests,
        "results":results
    }
    
    return render(request,"laboratory/completedreportsingle.html",context)
    


# patient Autocomplete on Order details 
def customer_autocomplete(request):
    if 'term' in request.GET:
        qs = Patient.objects.filter(first_name__icontains=request.GET.get('term')) | Patient.objects.filter(last_name__icontains=request.GET.get('term'))
        names = list()
        for patient in qs:
            names.append({
                'id': patient.id,
                'label': f"{patient.first_name} {patient.last_name}",
                'value': f"{patient.first_name} {patient.last_name}",
                'details': {
                    'first_name': patient.first_name,
                    'last_name': patient.last_name,
                    'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
                    'gender': patient.gender,
                    'address': patient.address,
                    'phone_number': patient.phone_number,
                    'email': patient.email,
                }
            })
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)


## customer adding to patient table and also the same patinet is to the order 

def Customer_adding_from_single_order(request,pk):
    order = Order.objects.get(id = pk)
    if request.method == "POST":
        # try:
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        age = request.POST.get('age')
        pnum = request.POST.get('pnum')
        email = request.POST.get('email')
        Address = request.POST.get('Address')
        slno = request.POST.get('slno')
        patient = Patient.objects.create(first_name = first_name, last_name = last_name,age = age,address = Address, phone_number = pnum, email = email, user = request.user,gender = slno)
        patient.save()
        order.patient = patient
        order.patient_name = patient.first_name + patient.last_name
        order.save()
        messages.success(request,"Patient Added")

        # except:
        #     print(request.data)
        #     messages.error(request,"something wrong")
        return redirect("OrderSingle",pk = pk)
    else:
        return redirect("OrderSingle",pk = pk)
    
@csrf_exempt   
def update_order_patient(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, id=pk)
        patient_id = request.POST.get('patient')
        
        if patient_id:
            try:
                patient = Patient.objects.get(id=patient_id)
                order.patient = patient
                order.patient_name = f"{patient.first_name} {patient.last_name}"
                order.save()
                return JsonResponse({'success': True})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt   
def update_order_sample(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, id=pk)
        sample = request.POST.get('sample')
        
        if sample:
            try:
                order.sample = sample
                order.save()
                return JsonResponse({'success': True})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}) 


@csrf_exempt   
def update_order_doctor(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, id=pk)
        doctor = request.POST.get('sample')
        
        if doctor:
            try:
                order.doctor = doctor
                order.save()
                return JsonResponse({'success': True})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}) 


@csrf_exempt   
def update_order_hospital(request, pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, id=pk)
        hospital = request.POST.get('sample')
        
        if hospital:
            try:
                order.hospital = hospital
                order.save()
                return JsonResponse({'success': True})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}) 

#pendingsample returns from pending samples we can view individal order
# NOTE: sample is sorted by order and filtered by creation user

def pending_samples(request):
    order =  Order.objects.filter(user = request.user,order_status = False)


    context = {
        "order":order
    }
    return render(request,"laboratory/pendingsamles.html",context)

def completed_samples(request):
    order =  Order.objects.filter(user = request.user,order_status = True)


    context = {
        "order":order
    }
    return render(request,"laboratory/completedsamples.html",context)



# test adding to order single add

@csrf_exempt
def addtest_ajax(request,pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, id=pk)
        testid = request.POST.get('testid')
        test = TestType.objects.get(id = testid)
        
        if test:
            try:
                result = TestResult.objects.create(order = order, test_type = test, technician = request.user, comments = "" )
                result.save()
                result = TestResult.objects.filter(order = order)
                testdeatil_table = render_to_string('ajaxtemplates/testdeatil_table.html', {'results': result})
                return JsonResponse({'success': True,"html": testdeatil_table})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}) 

@csrf_exempt
def conprehensive_addtest_ajax(request,pk):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        order = get_object_or_404(Order, id=pk)
        testid = request.POST.get('testid')
        test = ComprehensiveTest.objects.get(id = testid)
        
        if test:
            try:
                for i in test.tests.all():
                    result = TestResult.objects.create(order = order, test_type = i, technician = request.user, comments = "",comprehensive_test = test,is_comprehensive = True )
                    result.save()
                result = TestResult.objects.filter(order = order)
                testdeatil_table = render_to_string('ajaxtemplates/testdeatil_table.html', {'results': result})
                return JsonResponse({'success': True,"html": testdeatil_table})
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})




@csrf_exempt
def addresult_ajax(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        test_result_id = request.POST.get('resultid')
        print(test_result_id,"-----------------------------")
        test = TestResult.objects.get(id = int(test_result_id))
        result_value = request.POST.get('result')
        orderid = request.POST.get('orderId')
        order = Order.objects.get(id = orderid )
        if test:
            try:
                test.result_value = result_value
                test.save()
                result = TestResult.objects.filter(order = order)
                testdeatil_table = render_to_string('ajaxtemplates/testdeatil_table.html', {'results': result})
                return JsonResponse({'success': True})
                
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def addcomment_ajax(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        test_result_id = request.POST.get('resultid')
        print(test_result_id,"-----------------------------")
        test = TestResult.objects.get(id = int(test_result_id))
        result_value = request.POST.get('comment')
        orderid = request.POST.get('orderId')
        order = Order.objects.get(id = orderid )
        if test:
            try:
                test.comments = result_value
                test.save()
                result = TestResult.objects.filter(order = order)
                testdeatil_table = render_to_string('ajaxtemplates/testdeatil_table.html', {'results': result})
                return JsonResponse({'success': True})
                
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


def delete_test_result(request,pk):
    test = TestResult.objects.get(id = pk)
    order = test.order.id
    test.delete()
    messages.info(request,"Test Deleted...")
    return redirect("OrderSingle",pk = order)

def lab_report(request, pk):
    order = Order.objects.get(id=pk)
    results = TestResult.objects.filter(order=order)

    lab = {}
    try:
        lab = LabDetails.objects.get(user=request.user)
    except LabDetails.DoesNotExist:
        messages.warning(request, "Please fill out the address of the lab...")
        return redirect("profile")

    # Group the results by comprehensive_test (or None if it's not part of any comprehensive test)
    grouped_results = {"nocom":[]}
    for result in results:
        if result.comprehensive_test:
            if result.comprehensive_test not in grouped_results:
                grouped_results[result.comprehensive_test] = []
            grouped_results[result.comprehensive_test].append(result)
        else:
            if "nocom" not in grouped_results:
                grouped_results["nocom"] = []
            grouped_results["nocom"].append(result)

    print(grouped_results,"------------------")
    context = {
        "grouped_results": grouped_results,
        "order": order,
        "lab": lab,
    }
    return render(request, 'laboratory/labreport.html', context)

    
def lab_report_download(request,pk):
    order = Order.objects.get(id = pk) 
    result = TestResult.objects.filter(order = order)
    lab = {}
    try:
        lab = LabDetails.objects.get(user = request.user)
    except:
        messages.warning(request,"Please Fill out the address of the lab...")
        return redirect("profile")


    context = {
        "result":result,
        "order":order,
        "lab":lab
    }
    return render(request,'laboratory/labreport_pdf.html',context)

from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO

def labreportdownload(request,pk):
    # Render HTML content
    order = Order.objects.get(id = pk) 
    result = TestResult.objects.filter(order = order)
    lab = {}
    try:
        lab = LabDetails.objects.get(user = request.user)
    except:
        messages.warning(request,"Please Fill out the address of the lab...")
        return redirect("profile")
    context = {
        "result":result,
        "order":order,
        "lab":lab
    }
    html_string = render_to_string('laboratory/labreport.html', context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
    else:
        return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
from datetime import datetime

def ApproveReport(request,pk):
    order = Order.objects.get(id = pk)
    order.approvel_status = True
    order.order_status = True
    order.approval_date = datetime.now()
    order.save()
    return redirect("OrderSingleFinished",pk = pk )


def RecentlycompletedTests(request):
    order = Order.objects.filter(approval_date__gte = daybeforeyesterday, approval_date__lte = today, user = request.user)
    context = {
        "order":order
    }
    return render(request,"laboratory/recentlycompletedtests.html",context)

    








