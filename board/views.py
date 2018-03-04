from django.shortcuts import render, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from hitcount.views import HitCountDetailView
from ipware.ip import get_ip
from main.models import Board


class BoardList(ListView):
    template_name = 'board/list.html'

    def get_queryset(self):
        query_set = Board.objects.filter(category=self.kwargs.get('category'), display=True)
        if self.kwargs.get('category') == 'qna':
            query_set.filter(user=self.request.user.pk)
        return query_set

    def get_context_data(self, **kwargs):
        context = super(BoardList,self).get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context


class BoardDetail(LoginRequiredMixin, HitCountDetailView):
    template_name = 'board/detail.html'
    count_hit = True

    def get_queryset(self):
        query_set = Board.objects.filter(category=self.kwargs.get('category'), pk=self.kwargs.get('pk'), display=True)
        if self.kwargs.get('category') == 'qna':
            query_set.filter(user=self.request.user.pk)
        return query_set


# Create your views here.
class BoardEditor(LoginRequiredMixin, View):
    template_name = 'board/editor.html'

    def get(self, *args, **kwargs):
        context = {}
        if not self.request.user.extendsuser.nickname:
            messages.add_message(self.request, messages.INFO, "닉네임을 설정해야 글을 작성할 수 있습니다.")
            return HttpResponseRedirect(reverse('main:mypage'))
        context['category'] = self.kwargs.get('category')
        return render(self.request, self.template_name, context=context)

    def post(self, *args, **kwargs):
        if not self.request.user.extendsuser.nickname:
            messages.add_message(self.request, messages.INFO, "닉네임을 설정해야 글을 작성할 수 있습니다.")
            return HttpResponseRedirect(reverse('main:mypage'))
        board = Board.objects.create(
            title=self.request.POST.get('board_title'),
            detail=self.request.POST.get('board_detail'),
            user=self.request.user,
            ip=get_ip(self.request),
            category=self.kwargs.get('category'),
        )
        return HttpResponseRedirect(
            reverse('board:detail', kwargs={'pk': board.pk, 'category': self.kwargs.get('category')}))
