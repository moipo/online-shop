from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .forms import *
from .models import *
# Create your views here.

class Shop:
    def index(request):

        form = ProductModelForm()

        if request.method == "POST":
            form = ProductModelForm(request.POST)
            if form.is_valid():
                product = form.save()
                return redirect(product)

        ctx = {
        "product_form" : form
        }
        return render(request, "index.html", ctx)


    #def registration
    # def create_order(request):
    #     OrderFormSet = inlineformset_factory(Product, Order)
    #
