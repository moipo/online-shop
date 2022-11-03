from django.shortcuts import render, render
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
                redirect(product)

        ctx = {
        "form" : form
        }
        return render(request, "check.html", ctx)

    #def registration
