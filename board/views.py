import markdown2

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from hitcount.views import HitCountDetailView
from ipware.ip import get_ip
from main.models import Board


# Create your views here.
def macro_list(request):
    return render(request, 'board/macro_list.html')


# Create your views here.
class BoardList(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = Board
    template_name = 'board/board_list.html'

    def get_context_data(self, **kwargs):
        context = super(BoardList, self).get_context_data(**kwargs)
        context['board_list'] = Board.objects.all().order_by('-created')
        return context


class BoardDetail(LoginRequiredMixin, HitCountDetailView):
    login_url = '/accounts/login/'
    template_name = 'board/board_detail.html'
    model = Board
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(BoardDetail, self).get_context_data(**kwargs)
        return context


# Create your views here.
class BoardRegister(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    template_name = 'board/board_register.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        board = Board(
            title=self.request.POST.get('board_title'),
            detail=self.request.POST.get('board_detail'),
            user=self.request.user,
            ip=get_ip(self.request),
        )
        board.save()
        return HttpResponseRedirect(reverse('board:board_detail', kwargs={'pk': board.pk}))
