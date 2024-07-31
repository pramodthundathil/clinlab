from django.shortcuts import render, redirect
from .models import TestType, Order, TestResult
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from Home.models import Units, Patient, LabDetails
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string



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


# 3. Order Creation Sample Collection

def CreateSample(request):
    new_order = Order.objects.create(user = request.user )
    new_order.save()
    return redirect(OrderSingle,pk = new_order.id)


def OrderSingle(request,pk):
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
    return render(request,"laboratory/addsample.html",context) 


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
        patient = Patient.objects.create(first_name = first_name, last_name = last_name,age = age,address = Address, phone_number = pnum, email = email, user = request.user )
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
    order =  Order.objects.filter(user = request.user)


    context = {
        "order":order
    }
    return render(request,"laboratory/pendingsamles.html",context)



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

def lab_report(request,pk):
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
    return render(request,'laboratory/labreport.html',context)

    








