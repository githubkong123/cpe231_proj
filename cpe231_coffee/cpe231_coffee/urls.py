"""cpe231_coffee URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from report import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main,name='Main'),
    path('paymentform', views.payment_form, name='Paymenyform'),
    path('payment/list', views.PaymentList.as_view(), name='payment_list'), 
    # path('payment/get', views.payment), 
    path('payment/get/<payment_code>', views.PaymentGet.as_view(), name='payment_get'),
    path('payment/update', views.Paymentupdate.as_view(), name='payment_update'), 
    path('payment/save', views.PaymentSave.as_view(), name='payment_save'),   
    path('payment/save2', views.PaymentSave2.as_view(), name='payment_save2'), 
    path('payment/delete', views.PaymentDelete.as_view(), name='payment_delete'), 

    path('cashierform', views.cashier_form, name='Cashierform'),
    path('cashier/list', views.CashierList.as_view(), name='cashier_list'), 
    # path('payment/get', views.payment), 
    path('cashier/get/<cashier_id>', views.CashierGet.as_view(), name='cashier_get'),
    path('cashier/update', views.Cashierupdate.as_view(), name='cashier_update'), 
    path('cashier/save', views.CashierSave.as_view(), name='cashier_save'),   
    path('cashier/save2', views.CashierSave2.as_view(), name='cashier_save2'), 
    path('cashier/delete', views.CashierDelete.as_view(), name='cashier_delete'), 

    path('productform', views.product_form, name='Productform'),
    path('product/list', views.ProductList.as_view(),           name='product_list'), 
    # path('payment/get', views.payment), 
    path('product/get/<product_id>', views.ProductGet.as_view(),name='product_get'),
    path('product/update', views.Productupdate.as_view(),       name='product_update'), 
    path('product/save', views.ProductSave.as_view(),           name='product_save'),   
    path('product/save2', views.ProductSave2.as_view(),         name='product_save2'), 
    path('product/delete', views.ProductDelete.as_view(),       name='product_delete'), 

    path('ReportListAllOrders', views.ReportListAllOrders),
    path('ReportBestSellerOfTheDay', views.ReportBestSellerOfTheDay),
    path('ReportDetailOfProducts', views.ReportDetailOfProducts),
    
    path('Coffee_shop/product', views.ReportProductfrontend, name='Coffee_shop' ),
    path('coffeeshop/updatestock', views.ReportProductfrontend, name='update_stock' ),

    
]
