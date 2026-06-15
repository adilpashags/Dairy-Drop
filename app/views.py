from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import razorpay

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.conf import settings 
from .models import Product, Customer, Cart, OrderPlaced, Payment, Wishlist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect


# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    Wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request,"app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    totalitem = len(Cart.objects.filter(user=request.user))
    wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request,"app/contact.html",locals())


@method_decorator(login_required, name="dispatch")
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())

@method_decorator(login_required, name="dispatch")
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/category.html",locals())


@method_decorator(login_required, name="dispatch")
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.filter(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        product = Product.objects.get(pk=pk)
        return render(request,"app/productdetail.html",locals())
    


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        
        return render(request, 'app/customerregistration.html',locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Registration Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())
    


@method_decorator(login_required, name="dispatch")
class ProfileView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'

    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))

        customer = Customer.objects.filter(user=request.user).first()

        return render(request, 'app/profile.html', {
            'form': form,
            'customer': customer
        })

    def post(self, request):
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            user = request.user

            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                mobile=mobile,
                city=city,
                state=state,
                zipcode=zipcode
            )

            reg.save()

            messages.success(
                request,
                "Congratulations! Profile Saved Successfully"
            )

        else:
            messages.warning(request, "Invalid Input Data")

        customer = Customer.objects.filter(user=request.user).first()

        return render(request, 'app/profile.html', {
            'form': form,
            'customer': customer
        })
    

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/address.html', locals())

@method_decorator(login_required, name="dispatch")
class updateAddress(View):

    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
      
        return render(request, 'app/updateAddress.html', {'form': form})

    def post(self, request, pk):
        cust = Customer.objects.get(pk=pk)

        form = CustomerProfileForm(request.POST, instance=cust)

        if form.is_valid():
            form.save()
            messages.success(request, "Address Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect("address")
    


@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod-id')

    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    return render(request, 'app/addtocart.html', locals())



class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
       
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=("rzp_test_T1E2Bzc3iu3jIN", "mqM91avYs2pQdGQvJCzv8QUR"))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)

        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == "created":
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

            return render(request, 'app/checkout.html',locals())
    

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)

        wishlist = None
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(
                product=product,
                user=request.user
            )

            totalitem = Cart.objects.filter(
                user=request.user
            ).count()

            wishitem = Wishlist.objects.filter(
                user=request.user
            ).count()

        return render(request, 'app/productdetail.html', locals())


def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        c = Cart.objects.filter(
            product_id=prod_id,
            user=request.user
        ).first()

        if c:
            c.quantity += 1
            c.save()

        amount = 0
        cart = Cart.objects.filter(user=request.user)

        for p in cart:
            amount += p.quantity * p.product.discounted_price

        totalamount = amount + 40

        data = {
            'quantity': c.quantity if c else 0,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)




def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        c = Cart.objects.filter(
            product_id=prod_id,
            user=request.user
        ).first()

        if c and c.quantity > 1:
            c.quantity -= 1
            c.save()

        amount = 0
        cart = Cart.objects.filter(user=request.user)

        for p in cart:
            amount += p.quantity * p.product.discounted_price

        totalamount = amount + 40

        data = {
            'quantity': c.quantity if c else 0,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
    


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')

        c = Cart.objects.filter(
            Q(product_id=prod_id) &
            Q(user=request.user)
        )

        if c.exists():
            c.delete()

        amount = 0
        cart = Cart.objects.filter(user=request.user)

        for p in cart:
            amount += p.quantity * p.product.discounted_price

        totalamount = amount + 40

        data = {
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)



@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': op})



@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')

    user = request.user

    customer = Customer.objects.get(id=cust_id)

    payment = Payment.objects.get(razorpay_order_id=order_id)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart = Cart.objects.filter(user=user)

    for c in cart:
        OrderPlaced(
            user=user,
            customer=customer,
            product=c.product,
            quantity=c.quantity,
            payment=payment
        ).save()

        c.delete()

    return redirect("orders")


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist(user=user, product=product).save()

        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user

        Wishlist.objects.filter(
            user=user,
            product=product
        ).delete()

        data = {
            'message': 'Wishlist Remove Successfully',
        }
        return JsonResponse(data)
    

def show_wishlist(request):
    wishlist = Wishlist.objects.filter(user=request.user)

    totalitem = Cart.objects.filter(
        user=request.user
    ).count()

    wishitem = wishlist.count()

    return render(
        request,
        'app/wishlist.html',
        locals()
    )


@login_required
def search(request):
    query = request.GET.get('search')

    if not query:
        return redirect('/')

    product = Product.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )

    return render(request, 'app/search.html', locals())



def logout_confirm(request):
    logout(request)
    return redirect('home')