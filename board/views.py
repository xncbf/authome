from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from hitcount.views import HitCountDetailView
from ipware.ip import get_ip
from main.models import Board, ExtendsUser, UserPage


# Create your views here.
class MacroList(LoginRequiredMixin, ListView):
    template_name = 'board/macro_list.html'

    def get_queryset(self, **kwargs):
        return UserPage.objects.filter(user=self.request.user.pk)


# Create your views here.
class BoardList(ListView):
    model = Board
    template_name = 'board/board_list.html'

    def get_context_data(self, **kwargs):
        return super(BoardList, self).get_context_data(**kwargs)


class BoardDetail(LoginRequiredMixin, HitCountDetailView):
    template_name = 'board/board_detail.html'
    model = Board
    count_hit = True

    def get_context_data(self, **kwargs):
        return super(BoardDetail, self).get_context_data(**kwargs)


# Create your views here.
class BoardRegister(LoginRequiredMixin, View):
    template_name = 'board/board_register.html'

    def get(self, *args, **kwargs):
        context = {}
        try:
            if not self.request.user.extendsuser.nickname:
                raise ExtendsUser.DoesNotExist
        except ExtendsUser.DoesNotExist:
            messages.add_message(self.request, messages.INFO, "닉네임을 설정해야 글을 작성할 수 있습니다.")
            return HttpResponseRedirect(reverse('main:mypage'))
        return render(self.request, self.template_name, context=context)

    def post(self, *args, **kwargs):
        board = Board(
            title=self.request.POST.get('board_title'),
            detail=self.request.POST.get('board_detail'),
            user=self.request.user,
            ip=get_ip(self.request),
        )
        board.save()
        return HttpResponseRedirect(reverse('board:board_detail', kwargs={'pk': board.pk}))
