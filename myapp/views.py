from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Category, Product, Client, Order
from .forms import OrderForm, InterestForm, LoginForm
from datetime import date, datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    if 'last_login' in request.session :
        logininfo = request.session['last_login']
    else :
        logininfo = 'Your last login was more than an hour ago'
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'logininfo':logininfo})

def about(request):
    return render(request, 'myapp/about.html')

def about(request):
    visits = request.COOKIES.get('about_visits')
    if visits:
        response = render(request, 'myapp/about.html', {'about_visits': visits})
        response.set_cookie('about_visits', int(visits) + 1 , expires=300)
    else:
        response = render(request, 'myapp/about.html', {'about_visits': 1})
        response.set_cookie('about_visits', 1, expires=300 )

    return response

def detail(request, cat_no):
    category = get_object_or_404(Category, pk=cat_no)
    products = Product.objects.filter(category=category)
    return render(request, 'myapp/detail.html', {'category': category, 'products': products})

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST, initial={'status_date': date.today(), 'order_status': 'Order Placed'})
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                order.save()
                message = 'Your order has been placed successfully'
            else:
                if order.product.stock < 100:
                    Product.refill()
                message = 'Sorry, Not enough stock available! '
            return render(request, 'myapp/order_response.html', {'message': message})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'prodlist': prodlist})


def productdetail(request, prod_id):
    prod = Product.objects.get(pk=prod_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['interested'] == '1':
                prod.interested += 1
                prod.save()
            return redirect('/')

    else :
        form = InterestForm()
        return render(request, 'myapp/productdetail.html', {'form' : form, 'prod' : prod})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user :
            if user.is_active:
                if 'last_login' not in request.session :
                    request.session['last_login'] = str(datetime.now())
                    request.session.set_expiry(3600)
                login(request,user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled')
        else :
            return HttpResponse('Invalid Login details')
    else :
        return render(request, 'myapp/login.html', {'LoginForm': LoginForm})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required
def myorders(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        user_db = Client.objects.get(id=user_id)
        try:
            if user_db:
                order_list = list(Order.objects.filter(client=user_db))
            else:
                msg = 'There are no available orders!'
                return render(request, 'myapp/order_response.html', {'msg': msg})
        except:
            msg = 'You are not a registered client!'
            return render(request, 'myapp/order_response.html', {'msg': msg})

        return render(request, 'myapp/myorders.html', {'order_list': order_list})
    else:
        return redirect('login')