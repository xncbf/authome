from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
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


# Create your views here.
class BoardRegister(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    template_name = 'board/board_register.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name)

    def post(self, *args, **kwargs):
        # TODO: 게시글 등록 완료시 해당 게시물 페이지로 이동
        board = Board(
            title=self.request.POST.get('board_title'),
            detail=self.request.POST.get('board_detail'),
            user=self.request.user,
            ip=get_ip(self.request),
        )
        board.save()
        pass
