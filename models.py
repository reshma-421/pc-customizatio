from django.db import models

# Create your models here.
class userregister(models.Model):
    firstname=models.CharField(max_length=100,null=True,blank=True)
    lastname=models.CharField(max_length=100,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    age=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(upload_to='superman',null=True,blank=True)
    phonenumber=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return str(self.firstname)
    
class Feedback(models.Model):
    RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    ]
    
    feedback_text = models.TextField() 
    rating = models.IntegerField(choices=RATING_CHOICES) 
    created_at = models.DateTimeField(auto_now_add=True) 
    email=models.EmailField()
    def __str__(self):
        return self.email





class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()


    def __str__(self):
        return f"{self.name} - {self.subject}"


class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='pc',null=True,blank=True)
    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    rating = models.FloatField(null=True, blank=True)
    stock_status = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class addcart(models.Model):
     user = models.ForeignKey(userregister, on_delete=models.CASCADE)  
     product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
     stock_status = models.PositiveIntegerField(default=1)

class Payment(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)  # Reference to the user making the payment
    order_id = models.CharField(max_length=100)  # Order ID from Razorpay
    payment_id = models.CharField(max_length=100)  # Payment ID from Razorpay
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    currency = models.CharField(max_length=10)  # Currency (e.g., INR)
    payment_status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the payment was created

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} - Status: {self.payment_status}"
     
class Pre_Build(models.Model):
    Product_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    description = models.TextField(max_length=500)
    price=models.IntegerField()
    def __str__(self):
        return self.Product_name

    
    

class Payments(models.Model):
    product = models.ForeignKey(Pre_Build, on_delete=models.CASCADE)  # Link to the Pre_Build model
    price = models.IntegerField()  # Store the payment amount
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically store when the payment was made

    def __str__(self):
        return f"Payment of {self.price} for {self.product.Product_name}"



class Cart(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.firstname} - {self.product.name} - {self.quantity}"
class Payment(models.Model):
    user = models.ForeignKey(userregister, on_delete=models.CASCADE)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50)
    products = models.TextField()  # Store product information as a string (e.g., JSON)

    def __str__(self):
        return f"Payment {self.id} - {self.user}"