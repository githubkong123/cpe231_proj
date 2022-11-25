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


from report.models import *
import json
# Create your views here.

def ReportListAllOrders(request):
    cursor = connection.cursor()
    cursor.execute ('SELECT o.date as "Date", COUNT(o.order_id) as "Orders per day", SUM(o.total_order) as "Total order" '
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
                        ' JOIN "order" o ON o.order_id = oli.order_id '
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
    def get(self, request, order_id):
        orders = list(Order.objects.filter(
            order_id=order_id).values())
        data = dict()
        data['orders'] = orders

        return JsonResponse(data)




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'




@method_decorator(csrf_exempt, name='dispatch')
class OrderSave2(View):
    def post(self, request):
        data = dict()
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            data['error'] = form.errors
            return JsonResponse(data)

        orders = list(Order.objects.all().values())
        data['orders'] = orders

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)

import psycopg2
@method_decorator(csrf_exempt, name='dispatch')
class UpdateStock(View):
    def post(self, request):
        connection = psycopg2.connect(user="postgres",
                                        password="0507152035",
                                        host="localhost",
                                        database="CPE231")
        cursor = connection.cursor()
        data = json.loads(request.POST.get('lineitem', ''))
        # MyTable.objects.filter(pk=some_value).update(field1='some value')
        print(data)
        # for i in data:
        #     # query to update table with where clause
        #     sql='''update product set stock ='edit' WHERE product_id = %s; '''
        #     product_id = request.POST['product_id']

        #     # execute the query
        #     cursor.execute(sql,product_id)
        #     print('table updated..')

        #     print('table after updation...')
        #     sql2='''select * from payment_method;'''
        #     cursor.execute(sql2)

        #     # print table after modification
        #     print(cursor.fetchall())

        #     # Commit your changes in the database
        #     connection.commit()

        # # Closing the connection
        # connection.close()# code





# class OrderLineForm(forms.ModelForm):
#     class Meta:
#         model = OrderLineItem
#         fields = '__all__'





























































































































































































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
    
