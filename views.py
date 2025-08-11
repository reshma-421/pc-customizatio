from pyexpat.errors import messages
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .import models
from .models import Feedback,Contact,Category, Product, addcart,Pre_Build,userregister,Cart
from .models import*
import smtplib
import this
import razorpay
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
razorpay_client = razorpay.Client(
 auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.
def index(request):
    return render(request,'index.html')

def pc_home(request):
    return render(request,'pc_home.html')



def userregist(request):
    if(request.method=="POST"):
        firstname1=request.POST.get('firstname')
        lastname1=request.POST.get('lastname')
        email1=request.POST.get('email')
        age1=request.POST.get('age')
        password1=request.POST.get('password')
        image1=request.FILES.get('image')
        phonenumber=request.POST.get('phonenumber')
        if userregister.objects.filter(email=email1):
            alert="<script>alert('Email already exist');window.location.href='/userlogin/';</script>"
            return HttpResponse(alert) 
        object=userregister(firstname=firstname1,lastname=lastname1,email=email1,age=age1,password=password1,image=image1,phonenumber=phonenumber)
        object.save()
        
        return redirect('userlogin')
    return render(request,'userregister.html')
def userlogin(request):
    if request.method=="POST" :
        email2=request.POST.get('email')
        password2=request.POST.get('password')
        try:
            us=userregister.objects.get(email=email2,password=password2)
            semail=us.email
            request.session['email']=semail
            return redirect('userindex')
        except:
            msg="invalid username"
            return render(request,'userlogin.html',{"msg":msg})
    return render(request,'userlogin.html')

def profile(request):
    if 'email' in request.session:
        mail=request.session['email']
        usr=userregister.objects.get(email=mail)
    return render(request,'profile.html',{'usr':usr})


def editprofile(request,eid):
    edt=models.userregister.objects.get(id=eid)
    if request.method=='POST':
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        email=request.POST.get("email")
        age=request.POST.get("age")
        image=request.FILES.get('img')
        edt.firstname=firstname
        edt.lastname=lastname
        edt.email=email
        edt.age=age
        if image is not None:
            edt.image=image
        im=edt.image
        edt.image=im
        edt.save()
        return redirect('profile')
    return render(request,'editprofile.html',{'edt':edt})
def dashboard(request):
    return render(request,'dashboard.html')
# def pricing(request):
#     return render(request,'pricing.html')
# def payment(request):
#     return render(request,'payment.html')


def user_list(request):
    users = userregister.objects.all() 
    return render(request,'userlist.html', {'users': users})
def delete_user(request,did):
    x=models.userregister.objects.get(id=did)
    x.delete()
    return redirect('user_list')   

#adminlogin
def adminlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        e='admin@gmail.com'
        p='admin'
        if email==e:
            if password==p:
                return render(request,'dashboard.html')
    return render(request,'adminlogin.html')


#feedback used by user


from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def feedback(request):
    email = request.session.get('email')
    if email:
        # Fetch user information if logged in
        user = userregister.objects.filter(email=email).first()

        if request.method == "POST":
            feedback_text = request.POST.get('feedback_text')
            rating = request.POST.get('rating')
            email = request.POST.get('email')

            # Check if all fields are provided
            if not feedback_text or not rating or not email:
                alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/feedback_rate';</script>"
                return HttpResponse(alert_message)

            # Validate rating
            try:
                rating = int(rating)
                if rating not in [1, 2, 3, 4, 5]:
                    raise ValueError("Invalid rating value")
            except (ValueError, TypeError):
                alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/feedback_rate';</script>"
                return HttpResponse(alert_message)

            # Validate email format
            try:
                validate_email(email)
            except ValidationError:
                alert_message = "<script>alert('Please enter a valid email address.'); window.location.href='/feedback_rate';</script>"
                return HttpResponse(alert_message)

            # Create and save the Feedback instance
            feedback_instance = Feedback(
                feedback_text=feedback_text,
                rating=rating,
                email=email
            )
            feedback_instance.save()

            # Success message
            success_message = "<script>alert('Feedback submitted successfully!'); window.location.href='/feedback_rate';</script>"
            return HttpResponse(success_message)

        # Render the feedback form for GET requests, passing user data if available
        return render(request, 'feedback_rate.html', {'a': user})

    # Redirect if not logged in or email not in session
    alert_message = "<script>alert('Please log in to submit feedback.'); window.location.href='/login';</script>"
    return HttpResponse(alert_message)

    
#user index
def userindex(request):
    return render(request,'userindex.html')


#feedback list
def feedbacklist(request):
    data=Feedback.objects.all()
    return render(request,'feedbacklist.html',{'data':data})

#feedback delete

def feedbackdelete(request,did):
    x=models.Feedback.objects.get(id=did)
    x.delete()
    return redirect('feedbacklist')   










def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        contact_object = Contact(name=name, email=email, subject=subject, message=message)
        contact_object.save()
        
        
        return redirect('userindex') 

    return render(request, 'userindex.html')







def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, 'listmessage.html', {'contacts': contacts})



def logout(request):
    request.session.flush()
    return redirect('index')


def userlogout(request):
    request.session.flush()
    return redirect('index')




def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        
        if name:
            Category.objects.create(name=name, image=image)
            return redirect('dashboard')  # Redirect after successful addition

    return render(request, 'addcategory.html')


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        
        # Handling the image upload
        if category.image is not None:
            category.image = category.image
        # Save the updated product details
        category.save()
        return redirect('dashboard')
    
    return render(request, 'edit_category.html', {'c': category})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('dashboard')  # Replace with your redirect URL


# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'listcategory.html', {'categories': categories})




def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        discount_price = request.POST.get('discount_price') or None
        image = request.FILES.get('image')
        description = request.POST.get('description')
        rating = request.POST.get('rating') or None
        stock_status = int(request.POST.get('stock', 0))  # Ensure stock is an integer

        # Create a new Product instance
        Product.objects.create(
            name=name,
            category_id=category_id,
            price=price,
            discount_price=discount_price,
            image=image,
            description=description,
            rating=rating,
            stock_status=stock_status
        )

        return redirect('dashboard')  # Replace with your redirect URL

    categories = Category.objects.all()
    return render(request, 'addproduct.html', {'categories': categories})

def edit_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        category_id = request.POST.get('category')
        product.category = get_object_or_404(Category, id=category_id)
        
        product.price = request.POST.get('price')
        product.discount_price = request.POST.get('discount_price')
        product.stock_status = int(request.POST.get('stock') or 0)
        product.description = request.POST.get('description')
        product.rating = request.POST.get('rating')
        
        # Handling the image upload
        if product.image is not None:
            product.image = product.image
        # Save the updated product details
        product.save()
        return redirect('view_category')
    
    categories = Category.objects.all()
    return render(request, 'edit_product.html', {'p': product, 'categories': categories})









 


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
def view_category(request):
    categories = Category.objects.all()
    return render(request, 'view_category.html', {'categories': categories})

def product_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'product_list.html', {'category': category, 'products': products})

def view_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'view_products.html', {'category': category, 'products': products})


def error(request):
    return render(request,'error.html')




def addcarts(request, id):
    email = request.session['email']
    dt = Product.objects.get(id=id) 
    a = dt.name
    b = dt.category
    c = dt.price
    d = dt.discount_price
    f = dt.image.url  # Use .url to get the image URL
    return render(request, "addcart.html", {'a': a, 'b': b, 'c': c, 'e': email, 'd': d, 'f': f})



def add_cart(request):
    if request.method=='POST':
        name=request.POST.get('productname')
        producttype=request.POST.get('producttype')
        price=request.POST.get('price')
        
        stock_status=int(request.POST.get('stock_status'))
        data = Product.objects.get(name=name)

        a=data.stock_status
        b=int(a)
        newquantity=int(b-stock_status)
        
        c=request.session['email']
        cr=models.userregister.objects.get(email=c)
      
        if newquantity<0:
            return render(request,'error.html')
        else:
            data.stock_status=newquantity
            data.save()
        addcart(user=cr,product=data,stock_status=stock_status).save()
        return render(request,'userindex.html')
    else:
        return render(request,'addcart.html')

from django.shortcuts import render, redirect
from .models import addcart, Product  # Import your models

def view_cart(request):
    # Get the user's email from the session
    email = request.session.get('email')
    if not email:
        return redirect('login')  # Redirect to login if user is not logged in

    # Retrieve the user
    user = models.userregister.objects.get(email=email)

    # Get all items in the cart for the user
    cart_items = addcart.objects.filter(user=user)

    return render(request, 'cart.html', {'cart_items': cart_items})

def remove_from_cart(request, item_id):
    try:
        # Get the item to be removed from the cart
        item = addcart.objects.get(id=item_id)
        item.delete()  # Remove the item from the cart

        # Optionally, you can also restore the stock status if needed
        product = item.product
        product.stock_status += item.stock_status  # Restore the stock
        product.save()

        return redirect('view_cart')  # Redirect to the cart view after removing
    except addcart.DoesNotExist:
        return render(request, 'error.html', {'message': 'Item not found in cart.'})

from django.shortcuts import render, redirect
from .models import Payment, addcart  # Import your models
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def payment(request, order_id):  # Accepting order_id as a parameter
    email = request.session.get('email')
    if not email:
        return render(request, 'error.html', {'message': 'User not logged in.'})

    cr = addcart.objects.filter(user__email=email)  # Adjusted to filter by user
    totalprice = 0

    for item in cr:
        totalprice += int(item.product.price)  # Use the product's price
        item.delete()  # Remove from cart

    totalprice = int(totalprice * 100)  # Convert to smallest currency unit
    amount = int(totalprice)
    currency = 'INR'

    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment.html', context=context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment': payment_id,
                'razorpay_signature': signature
            }

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 20000  # Adjust this according to the actual payment amount
                try:
                    razorpay_client.payment.capture(payment_id, amount)

                    # Save payment details to the Payment model
                    Payment.objects.create(
                        user=request.user,  # Use the correct user instance
                        order_id=razorpay_order_id,
                        payment_id=payment_id,
                        amount=amount / 100,  # Convert back to the original amount
                        currency='INR',
                        payment_status='Completed'
                    )

                    return render(request, 'pay_success.html')
                except:
                    return render(request, 'pay_failed.html')
            else:
                return render(request, 'pay_failed.html')
        except Exception as e:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()



from django.shortcuts import render, redirect
from .models import Payment, addcart  # Import your models
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import addcart, Payment
import razorpay

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from .models import addcart, Payment
import razorpay

@csrf_exempt
def paymenthandler2(request):
    if request.method == "POST":
        try:
            print("POST data:", request.POST)  # Print POST data for debugging

            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            amount = request.POST.get('razorpay_amount', '0')

            # Log the amount received
            print("Received amount:", amount)

            # Check for missing payment data
            if not payment_id or not razorpay_order_id or not signature:
                print("Error: Missing payment data")
                return HttpResponseBadRequest("Missing payment data")

            # Validate amount format
            if not amount.isdigit():
                print("Error: Invalid amount format")
                return HttpResponseBadRequest("Invalid amount format.")

            # Convert amount to integer
            amount = int(amount)

            # Prepare parameters for payment signature verification
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # Verify the payment signature
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print("Signature verification result:", result)  # Debugging output

            if result is not None:
                try:
                    # Capture the payment
                    capture_response = razorpay_client.payment.capture(payment_id, amount)
                    print("Payment capture response:", capture_response)  # Debugging output

                    # Retrieve the user based on the session
                    user_email = request.session.get('email')
                    if user_email:
                        user = userregister.objects.get(email=user_email)
                    else:
                        print("Error: User not authenticated.")
                        return HttpResponseBadRequest("User not authenticated.")

                    # Save payment details in the Payment model
                    Payment.objects.create(
                        user=user,
                        order_id=razorpay_order_id,
                        payment_id=payment_id,
                        amount=float(amount) / 100,  # Convert back to rupees
                        currency='INR',
                        payment_status='Completed'
                    )

                    # Redirect to the success page
                    return render(request,'pay_success.html')  # Ensure this template exists

                except Exception as e:
                    print(f"Payment capture error: {str(e)}")
                    return render(request,'pay_success.html', {'error': "Payment capture failed."})

            else:
                print("Error: Signature verification failed.")
                return render(request,'pay_success.html', {'error': "Signature verification failed."})

        except Exception as e:
            print(f"Error processing payment: {str(e)}")
            return HttpResponseBadRequest("Error processing payment: " + str(e))

    return HttpResponseBadRequest("Invalid request method")


def payment2(request):
    email = request.session.get('email')
    if not email:
        return render(request, 'error.html', {'message': 'User not logged in.'})

    # Retrieve cart items for the user
    cart_items = addcart.objects.filter(user__email=email)
    total_price = 0

    # Calculate the total price, considering quantity and discount
    for item in cart_items:
        item_price = item.product.discount_price if item.product.discount_price else item.product.price
        total_price += item_price * item.stock_status

    # Convert to the smallest currency unit (paise for INR)
    amount = int(total_price * 100)
    currency = 'INR'

    # Check if the total meets Razorpay's minimum amount requirement (e.g., ₹1 or 100 paise)
    razorpay_minimum_amount = 100
    if amount < razorpay_minimum_amount:
        return render(request, 'error.html', {'message': 'Minimum payment amount is ₹1. Please add more items to your cart.'})

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create({
        'amount': amount,
        'currency': currency,
        'payment_capture': '0'
    })
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler2/'  # Ensure this matches the URL pattern in your app

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    # Clear the user's cart after calculating the total
    cart_items.delete()

    return render(request, 'payment.html', context=context)







def pay_failed(request):
    return render(request,'pay_failed.html')


def pay_success(request):
    return render(request,'pay_success.html')




def add_prebuild(request):
    if request.method == 'POST':
        # Get data from POST request
        product_name = request.POST.get('Product_name')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        price = request.POST.get('price')

        # Validation (optional)
        if product_name and image and description and price:
            # Convert price to integer (basic validation)
            try:
                price = int(price)
            except ValueError:
                # Handle invalid price input
                return render(request, 'add_prebuild.html', {
                    'error': 'Please enter a valid number for the price.',
                    'product_name': product_name,
                    'description': description,
                    'price': price,
                })
            
            # Create a new product instance
            new_product = Pre_Build(
                Product_name=product_name,
                image=image,
                description=description,
                price=price
            )
            new_product.save()  # Save to database
            
            # Redirect to a product list page or any other page
            return redirect('dashboard')  

        # If fields are missing, render the form again with an error
        return render(request, 'add_prebuild.html', {
            'error': 'All fields are required.',
            'product_name': product_name,
            'description': description,
            'price': price,
        })
    
    # Render the form on GET request
    return render(request, 'add_prebuild.html')

def prebuild_list(request):
    # Retrieve all Pre_Build products from the database
    products = Pre_Build.objects.all()
    
    # Pass the products to the 'product_list.html' template
    return render(request, 'prebuild_list.html', {'products': products})

def view_prebuild(request):
    # Retrieve all Pre_Build products from the database
    products = Pre_Build.objects.all()
    
    # Pass the products to the 'product_list.html' template
    return render(request, 'view_prebuild.html', {'products': products})



def search(request):
    if request.method == "POST":
        price = request.POST.get('price')
        if price:
            # Use case-insensitive filtering to improve user experience
            products = Pre_Build.objects.filter(price__icontains=price)
            
            # If no matching areas found, you can add a message
            if not products.exists():
                return render(request, 'search.html', {'message': 'No parking products found for the entered price', 'products': []})
            
            return render(request, 'search.html', {'products': products})
        else:
            # If the search input is empty
            return render(request, 'search.html', {'message': 'Please enter a valid price to search.'})
    
    else:
        return render(request, 'search.html')
    

from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Pre_Build, Payments  # Ensure the Payments model is imported
import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment3(request, id):
    email = request.session.get('email')  # Safely retrieve email from session
    donate = get_object_or_404(Pre_Build, id=id)  # Get the Pre_Build instance

    calculated_price = donate.price 

    # Create a new Payment instance with the product
    payment = Payments(product=donate, price=calculated_price)  # Link the product
    payment.save()  # Save the payment instance to the database

    totalprice = int(calculated_price * 100)  # Convert to paise
    currency = 'INR'

    # Create Razorpay order
    razorpay_order = razorpay_client.order.create(dict(amount=totalprice, currency=currency, payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler3/'  # Updated callback URL

    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': totalprice,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'payment.html', context=context)


@csrf_exempt
def paymenthandler3(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = request.POST.get('amount', 0)  # Get the amount from the request

                try:
                    razorpay_client.payment.capture(payment_id, amount)  # Capture the payment
                    return render(request, 'pay_success.html')
                except:
                    return render(request, 'pay_success.html')
            else:
                return render(request, 'pay_success.html')
        except Exception as e:
            print(f"Error: {e}")  # Log the exception for debugging
            return render(request, 'userindex.html')
    else:
        return render(request, 'userindex.html')


def delete_product(request, id):
    # Get the product or return a 404 if it doesn't exist
    product = get_object_or_404(Pre_Build, id=id)
    
    # Delete the product
    product.delete()
    
    # Redirect to the product list page (replace 'product_list' with your actual URL name)
    return redirect('view_prebuild') 


def delete_products(request, id):
    # Get the product or return a 404 if it doesn't exist
    product = get_object_or_404(Product, id=id)
    
    # Delete the product
    product.delete()
    
    # Redirect to the product list page (replace 'product_list' with your actual URL name)
    return redirect('dashboard') 

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Category, Product, Cart

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product, Cart
from django.utils import timezone

# This function handles rendering the page with products grouped by category.
def temp(request):
    categories = Category.objects.all()
    products_by_category = {}

    # Group products by category
    for category in categories:
        products_by_category[category.name] = Product.objects.filter(category=category)

    return render(request, 'temp.html', {
        'products_by_category': products_by_category,
    })

from django.core.exceptions import ValidationError

# This function handles adding products to the cart.
from django.utils import timezone

def add_to_cart(request):
    categories = Category.objects.all()
    products_by_category = {}

    # Group products by category
    for category in categories:
        products_by_category[category.name] = Product.objects.filter(category=category)

    # Handle adding to the cart
    if request.method == 'POST':
        # Initialize lists to hold selected product IDs and quantities
        product_ids = []
        quantities = []

        # Loop through categories to collect product IDs and quantities
        for category_name in products_by_category.keys():
            selected_product_id = request.POST.get(f'product_{category_name.lower()}')
            quantity = request.POST.get(f'quantity_{category_name.lower()}')

            # Skip if product is 'none', continue to the next category
            if selected_product_id == 'none':
                continue

            # Ensure valid product ID and quantity
            if not selected_product_id:  # Handle missing product ID
                messages.error(request, f"Please select a valid product for category: {category_name}.")
                return redirect('temp')

            if not quantity:
                messages.error(request, f"Please specify a quantity for product in category: {category_name}.")
                return redirect('temp')

            # Add the selected product and quantity to the lists
            product_ids.append(selected_product_id)
            quantities.append(quantity)

        # Check if product_ids and quantities are non-empty and aligned
        if not product_ids or not quantities:
            messages.error(request, "No products or quantities selected.")
            return redirect('temp')

        if len(product_ids) != len(quantities):
            messages.error(request, "Product and quantity mismatch.")
            return redirect('temp')

        success = False

        # Check if email is present in session and retrieve user
        if 'email' in request.session:
            email = request.session['email']
            try:
                user = userregister.objects.get(email=email)
            except userregister.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('login')  # Redirect to login if user not found
        else:
            messages.error(request, "User not logged in.")
            return redirect('login')  # Redirect to login if email is not in session

        # Process the selected products in bulk
        for product_id, quantity_str in zip(product_ids, quantities):
            try:
                # Validate and retrieve product
                product = Product.objects.get(id=product_id)

                # Try converting the quantity to an integer, and handle invalid cases
                try:
                    quantity = int(quantity_str)
                    if quantity <= 0:
                        raise ValueError("Quantity must be greater than zero.")
                except ValueError:
                    messages.error(request, f"Invalid quantity for product ID {product_id}. Please enter a valid number.")
                    return redirect('temp')

                # Calculate total price for the product
                total_price = product.price * quantity

                # Create or update the cart item
                cart_item, created = Cart.objects.get_or_create(
                    user=user,  # Use the user instance from the session
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'total_price': total_price,
                        'date_added': timezone.now()
                    }
                )

                if not created:
                    # Update the existing cart item with new quantity and price
                    cart_item.quantity += quantity
                    cart_item.total_price += total_price  # Add the total price to the existing one
                    cart_item.save()

                success = True
            except Product.DoesNotExist:
                messages.error(request, f"Product with ID {product_id} does not exist.")

        # Success or error message
        if success:
            messages.success(request, "Products added to the cart successfully.")
        else:
            messages.error(request, "No products were added to the cart. Please check your selections.")

        return redirect('my_cart')

    return render(request, 'temp.html', {
        'products_by_category': products_by_category,
    })


from django.shortcuts import render, get_object_or_404
from .models import userregister, Cart  # Assuming your models are in the same app

def cart_view(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, "You must be logged in to view the cart.")
        return redirect('login')  

    user = get_object_or_404(userregister, email=email)

    cart_items = Cart.objects.filter(user=user)

    total_price = sum(item.total_price for item in cart_items)


    return render(request, 'my_cart.html', {'cart_items': cart_items, 'total_price': total_price})


import smtplib
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Feedback

def confirmfeedback(request, f_id):
    data = get_object_or_404(Feedback, id=f_id)
    emaill = data.email
    print('Email address:', emaill)

    # Mark the feedback as accepted and save it
    data.is_accepted = True
    data.save()

    # Email details
    subject = "Feedback Confirmation"
    message = "We received your feedback and have accepted it. Thank you!"
    from_email = settings.DEFAULT_FROM_EMAIL

    try:
        # Send email using Django's send_mail function
        send_mail(subject, message, from_email, [emaill], fail_silently=False)
    except Exception as e:
        print("Failed to send email:", e)
    
    return redirect('feedbacklist')

from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from .models import Payment

from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from .models import userregister, Payment, Cart  # Assuming you have a Cart model for the user's cart

from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from .models import userregister, Payment, Cart  # Assuming you have a Cart model for the user's cart

def buy_product(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')  # Get total amount from the form
        c = request.session['email']
        user = userregister.objects.get(email=c)  # Assuming user ID is stored in session
        products = "[{\"product_id\": 1, \"quantity\": 2}, {\"product_id\": 2, \"quantity\": 1}]"  # Example product data

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({
            'amount': int(float(total_amount) * 100),  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Create the payment record
        payment = Payment.objects.create(
            user=user,
            total_amount=total_amount,
            razorpay_order_id=payment_order['id'],
            status='created',
            products=products  # Store product details as string
        )

        # Assuming payment is captured here; you can verify the payment status
        # Once payment is successful, delete items from the cart
          # Razorpay status verification should go here
            # Delete items from the cart after payment
            
        Cart.objects.filter(user=user).delete()  # Make sure to call delete() method here

        context = {
            'payment': payment_order,
            'razorpay_key_id': settings.RAZOR_KEY_ID,
            'price': total_amount
        }

        return render(request, 'buy.html', context)
    
    # Redirect to cart if method is not POST
    return redirect('my_cart')


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'successful'
        payment.save()
        return render(request, 'pay_success.html', {'payment': payment})
    return redirect('userindex')

