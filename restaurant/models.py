from django.db import models
import uuid


# Create your models here.
class Booking(models.Model):
   first_name = models.CharField(max_length=200)    
   last_name = models.CharField(max_length=200)
   guest_number = models.IntegerField()
   comment = models.CharField(max_length=1000)

   def __str__(self):
      return self.first_name + ' ' + self.last_name


# Add code to create Menu model
class Menu(models.Model):
   name = models.CharField(max_length=255)
   price = models.IntegerField()
   description = models.CharField(max_length=1000, default='')

   def __str__(self):
      return self.name
   
# Now we are adding the order class
class Order(models.Model):
   STATUS_CHOICES = [
      ('submitted', 'Submitted'),
      ('pending', 'Pending'),
      ('preparing', 'Preparing'),
      ('ready', 'Ready'),
      ('delivered','Delivered'),
      ('cancelled', 'Cancelled'),
   ]

   order_number = models.CharField(max_length=20, unique=True, blank=True)
   customer_name = models.CharField(max_length=200)
   customer_email = models.EmailField()
   note = models.CharField(max_length=500, blank=True)
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
   ordered_at = models.DateTimeField(auto_now_add=True)

   def save(self, *args, **kwargs):
      if not self.order_number:
         self.order_number = 'LL-' + str(uuid.uuid4())[:5].upper()
      super().save(*args, **kwargs)
   
   def __str__ (self):
      return f"Order {self.order_number} - {self.customer_name}"
   
   def get_total(self):
      return sum(items.get_subtotal() for item in self.items.all())
   
class OrderItem(models.Model):
   order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
   menu_item = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
   price_at_order = models.IntegerField()
   quatity = models.IntegerField(default=1)

   def get_subtotal(self):
      return self.price_at_order * self.quatity
   
   def __str__(self):
      return f"{self.quatity}x {self.menu_item.name}"
