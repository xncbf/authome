from django.shortcuts import render, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from hitcount.views import HitCountDetailView
from ipware.ip import get_ip
from main.models import Board, ExtendsUser, UserPage, Macro


# Create your views here.
class MacroList(LoginRequiredMixin, ListView):
    template_name = 'board/macro_list.html'

    def get_queryset(self, **kwargs):
        return UserPage.objects.filter(Q(user=self.request.user.pk) | Q(macro__user=self.request.user.pk))


class MacroBoardFree(LoginRequiredMixin, ListView):
    template_name = 'board/board_list.html'

    def get_queryset(self, **kwargs):
        query_set = Board.objects.filter(category=self.kwargs.get('pk'))
        if UserPage.objects.filter(macro_id=self.kwargs.get('pk')):
            return query_set
        else:
            raise Http404


class MacroBoardRegister(LoginRequiredMixin, View):
    template_name = 'board/board_register.html'

    def dispatch(self, request, *args, **kwargs):
        if UserPage.objects.filter(macro_id=self.kwargs.get('pk')):
            return super(MacroBoardRegister, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404

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
            category=kwargs.get('pk'),
        )
        board.save()
        return HttpResponseRedirect(reverse('board:board_detail', kwargs={'pk': board.pk}))



class BoardList(ListView):
    template_name = 'board/board_list.html'

    def get_queryset(self, **kwargs):
        return Board.objects.filter(category='free')


class BoardDetail(LoginRequiredMixin, HitCountDetailView):
    template_name = 'board/board_detail.html'
    count_hit = True

    def get_queryset(self, **kwargs):
        query_set = Board.objects.filter(pk=self.kwargs.get('pk'))
        # 자유게시판이 아닐 때 (매크로 게시판일 때)
        if query_set.first().category != 'free':
            macro = Macro.objects.filter(id=query_set.first().category).first()
            user_page = UserPage.objects.filter(macro_id=query_set.first().category).first()
            # 해당 매크로의 주인이거나 인증받은 내역이 있을 때
            if macro.user.pk == self.request.user.pk or user_page.user.pk == self.request.user.pk:
                return query_set
            else:
                raise Http404
        return query_set
        # return super(BoardDetail, self).get_context_data(**kwargs)


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
            category='free',
        )
        board.save()
        return HttpResponseRedirect(reverse('board:board_detail', kwargs={'pk': board.pk}))
