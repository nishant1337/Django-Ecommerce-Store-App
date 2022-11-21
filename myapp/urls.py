from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path(r'about', views.about, name='about'),
    path(r'<int:cat_no>/', views.detail, name='detail'),
    path(r'products/', views.products, name='products'),
    path(r'placeorder/',views.place_order,name='placeorder'),
    path(r'products/<int:prod_id>/', views.productdetail, name='productdetail'),
    path(r'accounts/login/', views.user_login, name='user_login'),
    path(r'logout', views.user_logout, name='user_logout'),
    path(r'myorders', views.myorders, name='myorders'),

]