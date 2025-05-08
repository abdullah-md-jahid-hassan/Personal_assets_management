from django.shortcuts import render
from django.http import HttpResponse

def opening_page(request):
    return render(request, 'opening_page.html')

