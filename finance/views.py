from django.shortcuts import render, redirect 
from .models import *
from Home.models import * 
from Clinic.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string




def Invoices(request):
    return render(request,"finance/invoices.html")

def Incomes(request):
    return render(request,"finance/income.html")


def Expenses(request):
    return render(request,"finance/expenses.html")


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
                table = render_to_string('ajaxtemplates/comprehensivetable.html', {'price': price})
                return JsonResponse({'status': 'success', 'html':table})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def get_invoice(request,pk):
    invoice = Invoce.objects.get(id = pk)
    invoice_items = InvoiceItems.objects.filter(invoice = invoice)

    context = {
        "invoice":invoice,
        "invoice_items":invoice_items
    }
    return render(request,"finance/invoice_sample.html",context)


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

