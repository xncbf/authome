from django.shortcuts import render

# Create your views here.


def tutorial(request):
    return render(request, 'docs/tutorial.html')


def introduction(request):
    return render(request, 'docs/introduction.html')
