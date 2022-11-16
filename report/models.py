from django.db import models

# Create your models here.


class Cashier(models.Model):
    cashier_id = models.CharField(max_length=20,primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20,null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    address = models.CharField(max_lenght=100,null=True, blank=True)
    class Meta:
        db_talbe = "cashier"
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
        
class Bill(models.Model):
    bill_id = models.CharField(max_length=20,primary_key=True)
    total_order = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True)
    cashier_id = models.ForeignKey(Cashier, on_delete=models.CASCADE, db_column='cashier_id')
    payment_method = models.ForeignKey(Payment, on_delete=models.CASCADE, db_column='payment_method')
    total_received = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "bill"
        managed = False
    def __str__(self):
        return self.bill_id

class Order(models.Model):
    order_id = models.CharField(max_length=20, primary_key =True)
    date = models.DateField(null=True)
    total_order = models.FloatField(null=True)
    class Meta:
        db_table = 'order'
        managed = False
    def __str__(self):
        return self.order_id

class OrderLineItem(models.Model):
    order_no = models.ForeignKey(Order, on_delete=models.CASCADE , db_column='order_no')
    item_no = models.IntegerField()
    product_id = models.ForeignKey(Order, on_delete=models.CASCADE , db_column='product_id')
    quantity = models.IntegerField()
    size = models.CharField(max_length=20)
    sugar_percentage = models.CharField(max_length=20)
    cashier_id = models.ForeignKey(Cashier, on_delete=models.CASCADE, db_column='cashier_id')
    class Meta:
        db_table = "order_line_item"
        managed = False
    def __str__(self):
        return '{"order_no":"%s","item_no":"%s","product_id":"%s","quantity":"%s", "size":"%s","sugar_percentage":"%s","cashier_id":"%s"}' % (self.order_no, self.item_no, self.item_no, 
        self.product_id, self.quantity,self.size,self.sugar_percentage,self.cashier_id)

class product(models.Model):
    product_id = models.CharField(max_length=20, primary_key= True)
    product_name = models.CharField(max_length = 50)
    stock = models.IntegerField()
    class Meta:
        db_table = 'product'
        managed = False
    def __str__(self):
        return self.order_id

class BillLineItem(models.Model):
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE, db_column='bill_id')
    item_no = models.CharField(max_length=20,null=True)
    order_id = models.CharField(Order, on_delete=models.CASCADE, db_column='order_id')
    
    class Meta:
        db_table = "bill_line_item"
        managed = False
    def __str__(self):
        return '{"bill_id":"%s","iten_no":"%s","order_id":"%s"}' % (self.bill_id, self.item_no, self.order_id)

class ProductLineItem(models.Model):
    product_id = models.ForeignKey(Bill, on_delete=models.CASCADE, db_column='product_id')
    product_size = models.CharField(max_length=10,null=True)
    product_type = models.CharField(max_length=15,null=True)
    product_cost = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = "prodcut_line_item"
        managed = False
    def __str__(self):
        return '{"product_id":"%s","product_size":"%s","product_type":"%s","product_cost":"%s"}' % (self.product_id, self.product_size, self.product_type, self.product_cost)









        



        








        

        
        

        