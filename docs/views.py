from django.shortcuts import render

# Create your views here.


def quick_start(request):
    return render(request, 'docs/quickstart.html')


def use_auth(request):
    return render(request, 'docs/use/autohotkey.html')


def introduction(request):
    return render(request, 'docs/introduction.html')
