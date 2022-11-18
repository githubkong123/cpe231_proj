from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import connection

from report.models import *
import json
# Create your views here.


def index(request):
    return render(request, 'forms_payment.html')


def payment(request):
    payment_method = request.GET.get('payment_method', '')
    payments = list(Cashier.objects.filter(
        payment_method=payment_method).values())
    data = dict()
    data['payments'] = payments

    return render(request, 'forms_payment.html', data)


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
class PaymentSave(View):
    def post(self, request):

        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        payments = list(Payment.objects.all().values())
        data = dict()
        data['payments'] = payments

        return render(request, 'forms_payment.html', data)

@method_decorator(csrf_exempt, name='dispatch')
class PaymentSave2(View):
    def post(self, request):

        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['customers'] = list()
            return JsonResponse(ret)

        payments = list(Payment.objects.all().values())
        data = dict()
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





























































































































































































# Task 1 ---
class CashierList(View):
    def get(self, request):
        cashiers = list(Cashier.objects.all().values())
        data = dict()
        data['cashiers'] = cashiers

        return JsonResponse(data)

# Task 2 ---
@method_decorator(csrf_exempt, name='dispatch')
class CashierSave(View):
    def post(self, request):
        
        print(request.POST)
        form = CashierForm(request.POST) 
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            return JsonResponse(ret)

        cashiers = list(Cashier.objects.all().values())
        data = dict()
        data['cashiers'] = cashiers
        
        return render(request, 'forms_cashier.html', data)

class CashierForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = '__all__'

# Task 3 ---
@method_decorator(csrf_exempt, name='dispatch')
class CashierSave2(View):
    def post(self, request):

        form = CashierForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            ret = dict()
            ret['result'] = form.errors
            ret['cashiers'] = list()
            return JsonResponse(ret)

        cashiers = list(Cashier.objects.all().values())
        data = dict()
        data['cashiers'] = cashiers

        return JsonResponse(data)
        #return render(request, 'forms_customer.html', data)
    
