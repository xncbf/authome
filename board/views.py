from django.shortcuts import render


# Create your views here.
def macro_list(request):
    return render(request, 'board/macro_list.html')


# Create your views here.
def board_list(request):
    return render(request, 'board/board_list.html')
