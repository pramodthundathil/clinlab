from django.shortcuts import render, redirect 
from .models import *
from Home.models import * 
from Clinic.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required




@login_required(login_url='SignIn')
def Invoices(request):
    invoices = Invoce.objects.filter(user=request.user).order_by("-date_time")

    context = {
        "invoices":invoices
    }
    return render(request,"finance/invoices.html",context)

@login_required(login_url='SignIn')
def Incomes(request):
    income = Income.objects.filter(user = request.user)
    if request.method == "POST":
        income_name = request.POST.get("income_name")
        income_amount = request.POST.get("amount")
        val = Income.objects.create(user = request.user,income_name = income_name,amount = income_amount)
        val.save()
        messages.success(request,"Income saved..")
        return redirect("Incomes")

    context = {
        "income":income
    }
    return render(request,"finance/income.html",context)

@login_required(login_url='SignIn')
def delete_income(request,pk):
    Income.objects.get(id = pk).delete()
    messages.success(request,"Income deleted..")

    return redirect("Incomes")

@login_required(login_url='SignIn')
def Expenses(request):
    expence = Expence.objects.filter(user = request.user)
    if request.method == "POST":
        income_name = request.POST.get("income_name")
        income_amount = request.POST.get("amount")
        val = Expence.objects.create(user = request.user,expence_name = income_name,amount = income_amount)
        val.save()
        messages.success(request,"Expence saved..")
        return redirect("Incomes")

    context = {
        "expence":expence
    }
    return render(request,"finance/expenses.html",context)

@login_required(login_url='SignIn')
def delete_expence(request,pk):
    Expence.objects.get(id = pk).delete()
    messages.success(request,"Expence deleted..")

    return redirect("Expenses")


@login_required(login_url='SignIn')
def Finance_settings(request):
    tests = TestType.objects.all()
    price = TestPriceSlab.objects.filter(user = request.user)
    context = {
        "tests":tests,
        "price":price
    }
    return render(request,"finance/finance_settings.html",context)


@csrf_exempt
def add_price_slab(request):
    if request.method == 'POST':
        test = request.POST.get('test')
        price1 = request.POST.get('price')
        price = TestPriceSlab.objects.filter(user = request.user)
        testval = TestType.objects.get(id = int(test))

        try:
            if TestPriceSlab.objects.filter(user = request.user,test = testval).exists():
                return JsonResponse({'status': 'error', 'message': "Test Price Already Exists...."})
            else:
                testval = TestType.objects.get(id = int(test))
                price_slab = TestPriceSlab(
                    test=testval,
                    price=price1,
                    user = request.user
                
                )
                price_slab.save()
                table = render_to_string('ajaxtemplates/priceslabtable.html', {'price': price})
                return JsonResponse({'status': 'success', 'html':table})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required(login_url='SignIn')
def get_invoice(request,pk):
    invoice = Invoce.objects.get(id = pk)
    invoice_items = InvoiceItems.objects.filter(invoice = invoice)
    lab = LabDetails.objects.get(user = request.user)

    context = {
        "invoice":invoice,
        "invoice_items":invoice_items,
        "lab":lab
    }
    return render(request,"finance/invoice_sample.html",context)


@login_required(login_url='SignIn')
def generete_invoice(request,pk):
    order =  Order.objects.get(id = pk)
    items = TestResult.objects.filter(order = order)
    try:
        invoice = Invoce.objects.create(order = order, user = request.user,total_payable = 0)
        invoice.save()
    except:
        if Invoce.objects.filter(order = order).exists():
            invoice = Invoce.objects.get(order = order)
        return redirect("get_invoice", pk = invoice.id )
    
    invoiceitems = []
    for i in items:
        print(i)
        if TestPriceSlab.objects.filter(test = i.test_type).exists():
            invoiceitems.append(TestPriceSlab.objects.get(test = i.test_type))
            continue
        else:
            slab = TestPriceSlab.objects.create(user = request.user, test = i.test_type, price = 0)
            slab.save()
            invoiceitems.append(slab)
            continue
    
    for j in invoiceitems:
        print(j,"oopweuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu",invoiceitems)
        invoice_items = InvoiceItems.objects.create(TestPrice = j, price = j.price, user = request.user, invoice = invoice)
        invoice_items.save()
        invoice.total_amount += j.price
        invoice.save()
        

    invoice.total_payable = invoice.total_amount - invoice.discount + invoice.adjustment
    invoice.save()

    return redirect("get_invoice", pk = invoice.id )

@csrf_exempt
def addprice_ajax(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        test_result_id = request.POST.get('resultid')
        print(test_result_id,"-----------------------------")
        test = TestPriceSlab.objects.get(id = int(test_result_id))
        result_value = request.POST.get('result')
        price = TestPriceSlab.objects.filter(user = request.user)
        
        if test:
            try:
                test.price = result_value
                test.save()
                
                testdeatil_table = render_to_string('ajaxtemplates/priceslabtable.html', {'price': price})
                return JsonResponse({'success': True,'html':testdeatil_table})
                
            except Patient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Patient does not exist'})
        else:
            return JsonResponse({'success': False, 'error': 'No patient selected'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required(login_url='SignIn')
def adjustment(request,pk):
    invoice = Invoce.objects.get(id = pk)
    if request.method == "POST":
        ajustments = request.POST.get('other_amount')
        discount = request.POST.get('discount')
        
        if ajustments:
            invoice.adjustment = float(ajustments)
        if discount:
            invoice.discount = float(discount)
        invoice.save()
        # invoiceitems = InvoiceItems.objects.filter(invoice = invoice )
            
        invoice.total_payable = invoice.total_amount - invoice.discount + invoice.adjustment
        invoice.save()

        print(ajustments, discount,"--------------------=======================")
    return redirect("get_invoice",pk = pk)


@login_required(login_url='SignIn')
def delete_invoice(request,pk):
    invoice = Invoce.objects.get(id = pk)
    invoice.delete()
    messages.info(request,"Invoice deleted")
    return redirect('Invoices')
