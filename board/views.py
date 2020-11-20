from django.shortcuts import render, redirect
from django.http import Http404
from member.models import BoardMember
from .models import Board
from .forms import BoardForm


def board_detail(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')
        # 게시물의 내용을 찾을 수 없을 때 내는 오류 message.

    return render(request, 'board_detail.html', {'board': board})


def board_list(request):
    boards = Board.objects.all().order_by('-id')
    return render(request, 'board_list.html', {"boards": boards})
    return redirect('/member/login/')


def board_write(request):
    if not request.session.get('user'):
        return redirect('/member/login/')
    # 세션에 'user' 키를 불러올 수 없으면, 로그인하지 않은 사용자이므로 로그인 페이지로 리다이렉트 한다.

    if request.method == "POST":
        form = BoardForm(request.POST)

        if form.is_valid():
            user_id = request.session.get('user')
            member = BoardMember.objects.get(pk=user_id)

            board = Board()
            board.title = form.cleaned_data['title']
            board.contents = form.cleaned_data['contents']
            board.writer = member
            board.save()

            return redirect('/board/list/')

    else:
        form = BoardForm()
        return render(request, 'board_write.html', {'form': form})
