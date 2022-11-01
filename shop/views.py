from django.shortcuts import render

# Create your views here.

class Shop:
    def index(request):
        return render(request, "index.html", {})
