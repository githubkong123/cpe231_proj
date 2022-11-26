from django.db import models

# Create your models here.


class Cashier(models.Model):
    cashier_id = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20,null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    class Meta:
        db_table = "cashier"
        managed = False
    def __str__(self):
        return self.cashier_id
    
class Payment(models.Model):
    payment_method = models.CharField(max_length=20, primary_key=True)
    payment_reference = models.CharField(max_length=100, null=True)
    class Meta:
        db_table = "payment"
        managed = False
    def __str__(self):
        return self.payment_method
        
class Product(models.Model):
    product_id = models.CharField(max_length=20, primary_key= True)
    product_name = models.CharField(max_length = 50)
    stock = models.IntegerField()
    description = models.CharField(max_length = 200)
    img_desc = models.CharField(max_length = 500)
    unit_price  = models.FloatField(null=True)
    class Meta:
        db_table = 'product'
        managed = False
    def __str__(self):
        return self.product_id

class Order(models.Model):
    order_no = models.CharField(max_length=20, primary_key =True)
    date = models.DateField(null=True)
    total_order = models.FloatField(null=True)
    cashier_id = models.ForeignKey(Cashier, on_delete=models.CASCADE, db_column='cashier_id')
    class Meta:
        db_table = 'order_n'
        managed = False
    def __str__(self):
        return self.order_no

class OrderLineItem(models.Model):
    order_no = models.ForeignKey(Order, on_delete=models.CASCADE , db_column='order_no')
    item_no = models.IntegerField()
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE , db_column='product_id')
    quantity = models.IntegerField()
    total_price = models.FloatField(null=True)
    class Meta:
        db_table = "order_line_item"
        unique_together = (("order_no", "item_no"),)
        managed = False
    def __str__(self):
        return '{"order_no":"%s","item_no":"%s","product_id":"%s","quantity":"%s","total_price":" %S}' % (self.order_no, self.item_no, self.item_no, 
        self.product_id, self.quantity,self.total_price)

class Bill(models.Model):
    bill_no = models.CharField(max_length=20,primary_key=True)
    payment_method = models.ForeignKey(Payment, on_delete=models.CASCADE, db_column='payment_method')
    order_no = models.CharField(max_length=20)
    class Meta:
        db_table = "bill"
        unique_together = (("order_no", "bill_no"),)
        managed = False
    def __str__(self):
        return self.bill_no


# class BillLineItem(models.Model):
#     bill_no = models.ForeignKey(Bill, on_delete=models.CASCADE, db_column='bill_no')
#     item_no = models.CharField(max_length=20,null=True)
#     order_no = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_no')
    
#     class Meta:
#         db_table = "bill_line_item"
#         managed = False
#     def __str__(self):
#         return '{"bill_no":"%s","iten_no":"%s","order_no":"%s"}' % (self.bill_no, self.item_no, self.order_no)

# class ProductLineItem(models.Model):
#     product_id = models.ForeignKey(Bill, on_delete=models.CASCADE, db_column='product_id')
#     product_size = models.CharField(max_length=10,null=True)
#     product_type = models.CharField(max_length=15,null=True)
#     product_cost = models.FloatField(null=True, blank=True)
    
#     class Meta:
#         db_table = "prodcut_line_item"
#         managed = False
#     def __str__(self):
#         return '{"product_id":"%s","product_size":"%s","product_type":"%s","product_cost":"%s"}' % (self.product_id, self.product_size, self.product_type, self.product_cost)









        



        








        

        
        

        