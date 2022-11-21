from django import forms
from myapp.models import Order, Client, Product, User
from django.core.validators import MinValueValidator


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']

    client = forms.ModelChoiceField(widget=forms.RadioSelect,queryset=Client.objects.all(),to_field_name="username",label='Client name')
    product = forms.ModelChoiceField(queryset=Product.objects.all().order_by('id'),to_field_name="name")
    num_units = forms.IntegerField(label='Quantity')


class InterestForm(forms.Form):
    INT_CHOICES = [(1, 'Yes'), (0, 'No')]
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=INT_CHOICES)
    quantity = forms.IntegerField(initial=1, min_value=1)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments', required=False)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
