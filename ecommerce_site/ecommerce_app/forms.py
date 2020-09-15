from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'arrival_date', 'price', 'inventory_count',
                  'brand', 'vendor', 'image', 'category']


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category']


class NewProductRequestForm(forms.ModelForm):
    class Meta:
        model = CustomerProductRequest
        fields = ['name', 'email', 'product_name', 'product_type',
                  'product_description']
