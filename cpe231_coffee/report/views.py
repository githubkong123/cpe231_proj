from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection
from django.db.models import Max
from django.db import transaction
from django.forms.models import model_to_dict
import re


from report.models import *
import json
# Create your views here.

def ReportListAllOrders(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT o.date as "Date", COUNT(o.order_no) as "Orders per day", SUM(o.total_order) as "Total order" '
                        ' FROM "order" as o '
                        ' GROUP BY o.date '
                        ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_list_all_orders.html', dataReport)

def ReportBestSellerOfTheDay(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT o.date as "Date", oli.product_id as "Product ID" , oli.quantity as "Quantity" '
                        ' FROM "order_line_item" as oli '
                        ' JOIN "order" o ON o.order_no = oli.order_no '
                        ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_best_seller_of_the_day.html', dataReport)

def ReportDetailOfProducts(request):
    cursor = connection.cursor()
    cursor.execute (' SELECT p.product_id as "Product ID" , p.product_name as "Product Name" ,  p.description as "Description" '
                        ' FROM "product" as p '
                        ' ')
    dataReport = dict()
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    dataReport['column_name'] = columns
    dataReport['data'] = CursorToDict(data,columns)

    return render(request, 'report_detail_of_products.html', dataReport)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result


def reFormatDateMMDDYYYY(ddmmyyyy):
        if (ddmmyyyy == ''):
            return ''
        return ddmmyyyy[3:5] + "/" + ddmmyyyy[:2] + "/" + ddmmyyyy[6:]

def reFormatNumber(str):
        if (str == ''):
            return ''
        return str.replace(",", "")

def main(request):
    return render(request, 'index.html')

def payment_form(request):
    return render(request, 'forms_payment.html')


# def payment(request):
#     payment_method = request.GET.get('payment_method', '')
#     payments = list(Cashier.objects.filter(
#         payment_method=payment_method).values())
#     data = dict()
#     data['payments'] = payments

#     return render(request, 'forms_payment.html', data)


class PaymentList(View):
    def get(self, request):
        payments = list(Payment.objects.all().values())
        data = dict()
        data['payments'] = payments

        return JsonResponse(data)


class PaymentGet(View):
    def get(self, request, payment_method):
        payments = list(Payment.objects.filter(
            payment_method=payment_method).values())
        data = dict()
        data['payments'] = payments

        return JsonResponse(data)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class Paymentupdate(View):
    @transaction.atomic
    def post(self, request):

        payment_method = request.POST['payment_method']

        payment = Payment.objects.get(payment_method=payment_method)
        request.POST = request.POST.copy()
        request.POST['payment_reference'] = request.POST['payment_reference']
        print(request.POST )


        data = dict()
        form = PaymentForm(instance=payment, data=request.POST)
        if form.is_valid():
            payments = form.save()

            data['payments'] = model_to_dict(payments)
        else:
            data['error'] = form.errors
            transaction.set_rollback(True)
            print (form.errors)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSave(View):
    def post(self, request):
        data = dict()
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['error'] = form.errors
            return JsonResponse(data)

        print('pass')

        payments = list(Payment.objects.all().values())
        data['payments'] = payments

        return render(request, 'forms_payment.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSave2(View):
    def post(self, request):
        data = dict()
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['error'] = form.errors
            return JsonResponse(data)

        payments = list(Payment.objects.all().values())
        data['payments'] = payments

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentDelete(View):
    def post(self, request):

        payment_method = request.POST['payment_method']
        payment = Payment.objects.get(payment_method=payment_method)
        data = dict()
        if payment:
            payment.delete()
            data['message'] = "Payment Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        payments = list(Payment.objects.all().values())
        data['payments'] = payments

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

#-------------------------Cashier


def cashier_form(request):
    return render(request, 'forms_cashier.html')


# def payment(request):
#     payment_method = request.GET.get('payment_method', '')
#     payments = list(Cashier.objects.filter(
#         payment_method=payment_method).values())
#     data = dict()
#     data['payments'] = payments

#     return render(request, 'forms_payment.html', data)


class CashierList(View):
    def get(self, request):
        cashiers = list(Cashier.objects.all().values())
        data = dict()
        data['cashiers'] = cashiers

        return JsonResponse(data)


class CashierGet(View):
    def get(self, request, cashier_id):
        cashiers = list(Cashier.objects.filter(
            cashier_id=cashier_id).values())
        data = dict()
        data['cashiers'] = cashiers

        return JsonResponse(data)


class CashierForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class Cashierupdate(View):
    @transaction.atomic
    def post(self, request):

        cashier_id = request.POST['cashier_id']

        cashier = Cashier.objects.get(cashier_id=cashier_id)
        request.POST = request.POST.copy()
        request.POST['name'] = request.POST['name']
        request.POST['phone'] = request.POST['phone']
        request.POST['salary'] = reFormatNumber(request.POST['salary'])
        request.POST['address'] = request.POST['address']

        print(request.POST )


        data = dict()
        form = CashierForm(instance=cashier, data=request.POST)
        if form.is_valid():
            cashiers = form.save()

            data['cashiers'] = model_to_dict(cashiers)
        else:
            data['error'] = form.errors
            transaction.set_rollback(True)
            print (form.errors)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class CashierSave(View):
    def post(self, request):
        data = dict()
        form = CashierForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['error'] = form.errors
            data['test'] = request.POST
            return JsonResponse(data)

        print('pass')

        cashiers = list(Cashier.objects.all().values())
        data['cashiers'] = cashiers

        return render(request, 'forms_cashier.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class CashierSave2(View):
    def post(self, request):
        data = dict()
        form = CashierForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['error'] = form.errors
            data['test'] = request.POST
            return JsonResponse(data)

        cashiers = list(Cashier.objects.all().values())
        data['cashiers'] = cashiers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class CashierDelete(View):
    def post(self, request):

        cashier_id = request.POST['cashier_id']
        cashier = Cashier.objects.get(cashier_id=cashier_id)
        data = dict()
        if cashier:
            cashier.delete()
            data['message'] = "cashier Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        cashiers = list(Cashier.objects.all().values())
        data['cashiers'] = cashiers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

#-------------------------------------------product

def product_form(request):
    return render(request, 'product_form.html')

class ProductList(View):
    def get(self, request):
        products = list(Product.objects.all().values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)


class ProductGet(View):
    def get(self, request, product_id):
        products = list(Product.objects.filter(
            product_id=product_id).values())
        data = dict()
        data['products'] = products

        return JsonResponse(data)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

@method_decorator(csrf_exempt, name='dispatch')
class Productupdate(View):
    @transaction.atomic
    def post(self, request):

        product_id = request.POST['product_id']

        product = Product.objects.get(product_id=product_id)
        request.POST = request.POST.copy()
        request.POST['product_name'] = request.POST['product_name']
        request.POST['stock'] = reFormatNumber(request.POST['stock'])
        request.POST['description'] = request.POST['description']
        request.POST['img_desc'] = request.POST['img_desc']
        request.POST['unit_price'] = reFormatNumber(request.POST['unit_price'])

        print(request.POST )


        data = dict()
        form = ProductForm(instance=product, data=request.POST)
        if form.is_valid():
            products = form.save()

            data['products'] = model_to_dict(products)
        else:
            data['error'] = form.errors
            transaction.set_rollback(True)
            print (form.errors)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class ProductSave(View):
    def post(self, request):
        data = dict()
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['test'] = request.POST
            return JsonResponse(data)

        print('pass')

        products = list(Product.objects.all().values())
        data['products'] = products

        return render(request, 'product_form.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class ProductSave2(View):
    def post(self, request):
        data = dict()
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['test'] = request.POST
            return JsonResponse(data)

        products = list(Product.objects.all().values())
        data['products'] = products

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class ProductDelete(View):
    def post(self, request):

        product_id = request.POST['product_id']
        product = Product.objects.get(product_id=product_id)
        data = dict()
        if product:
            product.delete()
            data['message'] = "product Deleted!"
        else:
            data['message'] = "Error!"
            return JsonResponse(data)

        products = list(Product.objects.all().values())
        data['products'] = products

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

def CursorToDict(data,columns):
    result = []
    fieldnames = [name.replace(" ", "_").lower() for name in columns]
    for row in data:
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result



def ReportProductfrontend(request):

    dataReport = dict()
    data = list(Product.objects.all().values())
    dataReport['data'] = data
    

    

    return render(request, 'templates_frontend/test_index.html', dataReport)



# def order_form(request):
#     return render(request, 'product_form.html')

class OrderList(View):
    def get(self, request):
        orders = list(Order.objects.all().values())
        data = dict()
        data['orders'] = orders

        return JsonResponse(data)


class OrderGet(View):
    def get(self, request, order_no):
        orders = list(Order.objects.filter(
            order_no=order_no).values())
        data = dict()
        data['orders'] = orders

        return JsonResponse(data)




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class OrderlineItemForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = '__all__'

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'


# @method_decorator(csrf_exempt, name='dispatch')
# class OrderSave2(View):
#     def post(self, request):
#         data = dict()
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             data['error'] = form.errors
#             return JsonResponse(data)

#         orders = list(Order.objects.all().values())
#         data['orders'] = orders

#         return JsonResponse(data)
#         #return render(request, 'forms_customer.html', data)
temp = ''

@method_decorator(csrf_exempt, name='dispatch')
class OrderCreate(View):

    @transaction.atomic
    def post(self, request):
        print(request.POST)
        print(json.loads(request.POST['lineitem']))
        if Order.objects.count() != 0:
            order_no_max = Order.objects.aggregate(Max('order_no'))['order_no__max']
            order_no_temp = [re.findall(r'(\w+?)(\d+)', order_no_max)[0]][0]   
            next_order_no = order_no_temp[0] + str(int(order_no_temp[1])+1) + "/22"
        else:
            next_order_no = "OD100/22"

        global temp
        if next_order_no != '':
            temp = next_order_no

        print(next_order_no)

        request.POST = request.POST.copy()
        request.POST['order_no'] = next_order_no
        request.POST['date'] = reFormatDateMMDDYYYY(request.POST['date'])
        request.POST['total_order'] = reFormatNumber(request.POST['total_order'])
        request.POST['cashier_id'] = request.POST['cashier_id']


        
        data = dict()
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            OrderLineItem.objects.filter(order_no=next_order_no).delete()
            dict_lineitem = json.loads(request.POST['lineitem'])
            for lineitem in dict_lineitem['lineitem']:
                lineitem['order_no'] = next_order_no
                lineitem['quantity'] = reFormatNumber(lineitem['quantity'])
                lineitem['total_price'] = reFormatNumber(lineitem['total_price'])
                pre_stock =  Product.objects.filter(product_id= lineitem['product_id']).values()[0]['stock'] - int(lineitem['quantity'])
                print('pre_stock= ',pre_stock)
                Product.objects.filter(product_id= lineitem['product_id']).update(stock = pre_stock)

                print(lineitem)
                formlineitem = OrderlineItemForm(lineitem)
                
                try:
                    formlineitem.save()
                except:
                    data['error'] = formlineitem.errors
                    print(formlineitem.errors)
                    transaction.set_rollback(True)

            data['order'] = model_to_dict(order)
        else:
            # if invoice from is not valid return error message
            data['error'] = form.errors
            print (form.errors)
        
        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class BillCreate(View):
    def post(self, request):
        # if Order.objects.count() != 0:
        #     order_no_max = Order.objects.aggregate(Max('order_no'))['order_no__max']
        #     order_no_temp = [re.findall(r'(\w+?)(\d+)', order_no_max)[0]][0]   
        #     select_order_no = order_no_temp[0] + str(int(order_no_temp[1])) + "/22"
        # else:
        #     select_order_no = "OD100/22"

        if Bill.objects.count() != 0:
                bill_no_max = Bill.objects.aggregate(Max('bill_no'))['bill_no__max']
                bill_no_temp = [re.findall(r'(\w+?)(\d+)', bill_no_max)[0]][0]   
                next_bill_no = bill_no_temp[0] + str(int(bill_no_temp[1])+1) + "/22"
        else:
            next_bill_no = "BT100/22"

        print('bill--------------------------')
        # if Order.objects.count() != 0:
        #     order_no_max = Order.objects.aggregate(Max('order_no'))['order_no__max']
        #     order_no_temp = [re.findall(r'(\w+?)(\d+)', order_no_max)[0]][0]   
        #     select_order_no = order_no_temp[0] + str(int(order_no_temp[1])) + "/22"
        # else:
        #     select_order_no = "OD100/22"

        # print(select_order_no)
        print(temp)

        request.POST = request.POST.copy()
        request.POST['payment_method'] = request.POST['payment_method']
        request.POST['bill_no'] = next_bill_no
        request.POST['order_no'] = temp

        data = dict()
        form_bill = BillForm(request.POST)
        if form_bill.is_valid():
            bill = form_bill.save()
            data['bill'] = model_to_dict(bill)
        else:
            # if invoice from is not valid return error message
            data['error'] = form_bill.errors
            print (form_bill.errors)

        return JsonResponse(data)


        


        




























































































































































































# # Task 1 ---
# class CashierList(View):
#     def get(self, request):
#         cashiers = list(Cashier.objects.all().values())
#         data = dict()
#         data['cashiers'] = cashiers

#         return JsonResponse(data)

# # Task 2 ---
# @method_decorator(csrf_exempt, name='dispatch')
# class CashierSave(View):
#     def post(self, request):
        
#         print(request.POST)
#         form = CashierForm(request.POST) 
#         if form.is_valid():
#             form.save()
#         else:
#             ret = dict()
#             ret['result'] = form.errors
#             return JsonResponse(ret)

#         cashiers = list(Cashier.objects.all().values())
#         data = dict()
#         data['cashiers'] = cashiers
        
#         return render(request, 'forms_cashier.html', data)

# class CashierForm(forms.ModelForm):
#     class Meta:
#         model = Cashier
#         fields = '__all__'

# # Task 3 ---
# @method_decorator(csrf_exempt, name='dispatch')
# class CashierSave2(View):
#     def post(self, request):

#         form = CashierForm(request.POST)
#         if form.is_valid():
#             form.save()
#         else:
#             ret = dict()
#             ret['result'] = form.errors
#             ret['cashiers'] = list()
#             return JsonResponse(ret)

#         cashiers = list(Cashier.objects.all().values())
#         data = dict()
#         data['cashiers'] = cashiers

#         return JsonResponse(data)
#         #return render(request, 'forms_customer.html', data)
    
