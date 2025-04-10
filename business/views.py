from django.http import HttpResponse
from django.shortcuts import render

from business.models import Business


# Create your views here.

def index(request):
    businesses = Business.objects.order_by('-name')
    print(", ".join([f"{b.name} ({b.location})" for b in businesses]))
    context = {"businesses": businesses}
    return render(request, "business/index.html", context)

def detail(request, id):
    return HttpResponse("You're looking at business %s." % id)