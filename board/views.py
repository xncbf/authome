from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View

from pure_pagination.mixins import PaginationMixin
from hitcount.views import HitCountDetailView
from ipware.ip import get_ip

from authome.settings import SERVER_EMAIL

from main.models import Board


class BoardList(PaginationMixin, ListView):
    template_name = 'board/list.html'
    paginate_by = 10

    def get_queryset(self):
        query_set = Board.objects.filter(category=self.kwargs.get('category'), display=True)
        if self.kwargs.get('category') == 'qna':
            if not self.request.user.id:
                query_set = Board.objects.filter(id=-1)
            else:
                if self.request.user.email != SERVER_EMAIL:
                    query_set = query_set.filter(user=self.request.user.pk)
        s = self.request.GET.get('s')
        if s:
            query_set = query_set.filter(Q(title__icontains=s) | Q(detail__icontains=s))
        return query_set

    def get_context_data(self, **kwargs):
        context = super(BoardList, self).get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context


class BoardDetail(LoginRequiredMixin, HitCountDetailView):
    template_name = 'board/detail.html'
    count_hit = True

    def get_queryset(self):
        query_set = Board.objects.filter(category=self.kwargs.get('category'), pk=self.kwargs.get('pk'), display=True)
        if self.kwargs.get('category') == 'qna':
            if self.request.user.email != SERVER_EMAIL:
                query_set = query_set.filter(user=self.request.user.pk)
        return query_set

    def get_context_data(self, **kwargs):
        context = super(BoardDetail, self).get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context


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
