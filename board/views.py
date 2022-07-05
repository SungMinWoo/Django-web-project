# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.db.models import Q, F, Count
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone

from .forms import BoardWriteForm
from .models import Board, Reply, Report
from accounts.models import User
from public_function.public_func import paginator_func, divide_board, delete_img_s3
from public_function.decorator import block_ip
from public_function.public_data import BLOCK_TIME, IP
from public_function.decorator import login_required

from ratelimit.decorators import ratelimit
from datetime import timedelta

import json
import datetime


# 게시판 검색 함수
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def search_list(request, categories, keyword): # 검색 결과 함수
    if keyword: # 키워드가 있다면
        question_list = categories.filter(
            Q(poli_nm__icontains=keyword)
        ).distinct() # 키워드에 대한 검색 결과 poli_nm이 포함된 키워드
        politic_list = paginator_func(request, question_list)
        if len(politic_list) == 0:
            message = keyword + '로 검색된 결과가 없습니다.'
        else:
            message = keyword + ' 검색 결과입니다.'
        poli_info = {
            'politic_list': politic_list,
            'message': message,
        }
    else: # 키워드가 없다면
        message = '검색어를 입력해주세요'
        poli_info = {
            'message': message,
        }

    return poli_info


# 게시글 리스트
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_list(request, board_type=None):
    if request.method == 'GET':
        board_data = Board.objects.filter(board_id=board_type).order_by('post_create').annotate(reply_count=Count(F('reply')))[::-1] # 역참조로 댓글 갯수 확인
        board_data = paginator_func(request, board_data, 20)
        board_type_kr = divide_board(board_type, True)

        best_data = Board.objects.filter(board_id=board_type).filter(post_create__gte=timezone.localtime() - timedelta(days=7)).annotate(num_like=Count('post_like')).filter(num_like__gte=10).order_by('-num_like')[:5]
        if best_data:
            best_data = reversed(best_data.annotate(reply_count=Count(F('reply')))[::-1])

        return render(request, 'board/board.html', {'board_data': board_data, 'board_type':board_type_kr, 'board_type_en':board_type, 'best_post': best_data})


# 게시글 내 검색
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_search(request, board_type=None): # 게시판 검색
    keyword = request.GET.get('search')
    choice = request.GET.get('choice')

    board_data = Board.objects.filter(board_id=board_type)
    if choice == 'title_content':
        board_data = board_data.filter(Q(post_title__icontains=keyword) | Q(post_content__icontains=keyword)).annotate(
            reply_count=Count(F('reply')))[::-1]
    elif choice == 'title':
        board_data = board_data.filter(Q(post_title__icontains=keyword)).annotate(
            reply_count=Count(F('reply')))[::-1]
    elif choice == 'content':
        board_data = board_data.filter(Q(post_content__icontains=keyword)).annotate(
            reply_count=Count(F('reply')))[::-1]
    elif choice == 'writer':
        board_data = board_data.filter(Q(post_writer__nickname__icontains=keyword)).annotate(
            reply_count=Count(F('reply')))[::-1]
    board_data = paginator_func(request, board_data, 10)
    board_type_kr = divide_board(board_type, True)
    return render(request, 'board/board.html',
                  {'board_data': board_data, 'board_type': board_type_kr,
                   'board_type_en': board_type, 'search': keyword, 'choice':choice})


# 게시글 쓰기 board_type은 게시판 졸유
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_write(request, board_type=None):
    session = request.session.get('authUser')
    context = {'login_session': session['nickname']}

    login_session = session['like']

    if login_session == '중도' and board_type[0:3] == 'opp' or login_session == '중도' and board_type[0:3] == 'rul': # 글쓰기 권한 나누기
        messages.warning(request, '글쓰기 권한이 존재하지 않습니다.')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found')) # 이전페이지로 이동
    elif login_session == '진보' and board_type[0:3] == 'rul':
        messages.warning(request, '글쓰기 권한이 존재하지 않습니다.')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    elif login_session == '보수' and board_type[0:3] == 'opp':
        messages.warning(request, '글쓰기 권한이 존재하지 않습니다.')
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    if request.method == 'GET':
        write_form = BoardWriteForm()
        context['forms'] = write_form
        board_type = divide_board(board_type, True)
        not_board_type = divide_board(board_type, False)
        context['board_type'] = board_type
        context['not_board_type'] = not_board_type

        return render(request, 'board/board_write.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)

        if write_form.is_valid():
            writer = User.objects.get(nickname=session['nickname'])
            board = Board(
                post_title=write_form.post_title,
                post_content=write_form.post_content,
                post_writer=writer,
                board_id=board_type,
            )
            board.save()
            return redirect('board:board', board_type)
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_write.html', context)


# 게시글 취소시 이미지 체크
def check_img(request):
    html_code = request.POST.dict()
    delete_img_s3([html_code['code']]) # 리스트 형식으로 전달
    result = {
        'result': 'success',
    }
    return JsonResponse(result)


# 게시글 업데이트
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_update(request, pk=None):
    session = request.session.get('authUser')
    context = {'login_session': session['nickname']}

    board = get_object_or_404(Board, id=pk)
    board_type = board.board_id
    context['board'] = board

    if board.post_writer.nickname != session['nickname']:
        return redirect(f'/board/board_detail/{pk}')

    if request.method == 'GET':
        write_form = BoardWriteForm(instance=board)
        context['forms'] = write_form
        board_type = divide_board(board_type, True)
        not_board_type = divide_board(board_type, False)
        context['board_type'] = board_type
        context['not_board_type'] = not_board_type
        return render(request, 'board/board_update.html', context)

    elif request.method == 'POST':
        write_form = BoardWriteForm(request.POST)
        now = datetime.datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')
        if write_form.is_valid():
            board.post_title = write_form.post_title
            board.post_content = write_form.post_content
            board.board_id = board_type
            board.post_update = time # 댓글 수정시
            board.save()
            return redirect('board:board', board_type)
        else:
            context['forms'] = write_form
            if write_form.errors:
                for value in write_form.errors.values():
                    context['error'] = value
            return render(request, 'board/board_write.html', context)


# 게시글 세부 내용
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_detail(request, pk):
    board = get_object_or_404(Board, id=pk)
    re_replys = Reply.objects.filter(reply_post=pk, reply_parent__isnull=False)
    board_type = divide_board(board.board_id, True)  # 게시판 정보 한글

    context = {'detail':board}

    context['board_type'] = board_type
    if request.GET.get('search'):
        context['redirect'] = f'{request.GET.get("next")}&choice={request.GET.get("choice")}&search={request.GET.get("search")}'
    else:
        context['redirect'] = request.GET.get('next')

    best_reply = Reply.objects.filter(reply_post=pk).annotate(num_like=Count('reply_like')).filter(num_like__gte=10).order_by('-num_like')[:3]
    context['best_reply'] = best_reply

    if request.method == 'GET':
        reply = Reply.objects.filter(reply_post=pk, reply_parent__isnull=True)

        re_reply_list = list()
        for re_reply in re_replys:
            re_reply_list.append(re_reply.reply_parent.id)

        reply_count = len(reply) + len(re_replys)
        reply_pag = paginator_func(request, reply, 5)  # 댓글 페이지
        context['re_reply_list'] = re_reply_list
        context['reply_count'] = reply_count
        context['re_reply'] = re_replys
        context['reply'] = reply_pag

        board.post_views += 1  # 조회수 클릭당 1
        board.save()
        if request.session.get('authUser'):
            session = request.session.get('authUser')['nickname']
            context['login_session'] = session
            try:
                if board.post_writer.nickname == session:  # 글쓴 유저가 같으면 수정, 삭제버튼 보이게
                    context['writer'] = True
                else:
                    context['writer'] = False
            except:
                context['writer'] = False
            return render(request, 'board/board_detail.html', context)
        else:
            return render(request, 'board/board_detail.html', context)
    elif request.method == 'POST':
        if request.POST.get('choice'): # 댓글 정렬
            value = request.POST.get('choice')
            if value == 'new':
                reply = Reply.objects.filter(reply_post=pk, reply_parent__isnull=True)
            elif value == 'most_like':
                reply = Reply.objects.filter(reply_post=pk, reply_parent__isnull=True).annotate(num_like=Count('reply_like')).order_by('-num_like')
            elif value == 'most_dislike':
                reply = Reply.objects.filter(reply_post=pk, reply_parent__isnull=True).annotate(num_dislike=Count('reply_dislike')).order_by('-num_dislike')
            reply_pag = paginator_func(request, reply, 15)  # 댓글 페이지
            reply_count = len(reply) + len(re_replys)
            context['reply_count'] = reply_count
            context['re_reply'] = re_replys
            context['reply'] = reply_pag
            context['select'] = value
            return render(request, 'board/board_detail.html', context)
        elif request.POST.get('report_board'):
            report_type = request.POST.get('report_board')
            nick = request.session.get('authUser')['nickname']

            board_id = Board.objects.get(id=pk)
            report_user = User.objects.get(nickname=nick)
            save_report = Report(
                report_post=board_id,
                report_reason=report_type,
                report_user=report_user,
            )
            save_report.save()
            return redirect(request.build_absolute_uri())
        elif request.POST.get('report_reply'):
            reply_id = request.POST.get('report_reply_id')
            report_type = request.POST.get('report_reply')
            nick = request.session.get('authUser')['nickname']

            board_id = Board.objects.get(id=pk)
            reply_id = Reply.objects.get(id=reply_id)
            report_user = User.objects.get(nickname=nick)
            save_report = Report(
                report_post=board_id,
                report_reply=reply_id,
                report_reason=report_type,
                report_user=report_user,
            )
            save_report.save()
            return redirect(request.build_absolute_uri())

        if request.session.get('authUser'):
            nick = request.session.get('authUser')['nickname']
            nickname = User.objects.get(nickname=nick)
            board_id = Board.objects.get(id=pk)
            if request.POST.get('reply_content'):
                content = request.POST.get('reply_content')
                save_reply = Reply(
                    reply_contents=content,
                    reply_writer=nickname,
                    reply_post=board_id,
                )
                save_reply.save()
                return redirect(request.build_absolute_uri())
            elif request.POST.get('re_reply_content'):
                content = request.POST.get('re_reply_content')
                reply_id = request.POST.get('re_reply_id')
                reply_id = Reply.objects.get(id=reply_id)
                save_reply = Reply(
                    reply_contents=content,
                    reply_writer=nickname,
                    reply_post=board_id,
                    reply_parent=reply_id
                )

                save_reply.save()
                return redirect(request.build_absolute_uri())


# 게시글 삭제
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_delete(request, pk):
    session = request.session.get('authUser')
    board = get_object_or_404(Board, id=pk)
    if board.post_writer.nickname == session['nickname']:
        delete_img_s3(board.post_content)
        board.delete()
        return redirect(f'/board/board/{board.board_id}')
    else: # url을 통해 강제로 삭제 시 해당페이지로 다시 보냄
        return redirect(f'/board/board_detail/{pk}')


# 댓글 삭제
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def reply_delete(request, pk, id):
    session = request.session.get('authUser')
    reply = Reply.objects.get(id=id)
    if reply.reply_writer.nickname == session['nickname']:
        reply.delete()
        return redirect(f'/board/board_detail/{pk}')
    else: # url을 통해 강제로 삭제 시 해당페이지로 다시 보냄
        return redirect(f'/board/board_detail/{pk}')


# 댓글 업데이트
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def reply_update(request, pk, id):
    session = request.session.get('authUser')
    reply = Reply.objects.get(id=id)
    now = datetime.datetime.now()
    time = now.strftime('%Y-%m-%d %H:%M:%S')
    if reply.reply_writer.nickname == session['nickname']:
        content = request.POST.get(str(id))
        reply.reply_contents = content
        reply.reply_update = time # 댓글 수정 시
        reply.save()
        return redirect(f'/board/board_detail/{pk}')
    else:  # url을 통해 강제로 삭제 시 해당페이지로 다시 보냄
        return redirect(f'/board/board_detail/{pk}')


# 게시물 좋아요
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_likes(request, pk):
    post = Board.objects.get(id=pk)
    likes = LikeFunction(request, post.board_id, post.post_like, post.post_dislike)
    return HttpResponse(json.dumps(likes.post_like()), content_type='application/json')


# 게시물 싫어요
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def post_dislikes(request, pk):
    post = Board.objects.get(id=pk)
    dislikes = LikeFunction(request, post.board_id, post.post_like, post.post_dislike)
    return HttpResponse(json.dumps(dislikes.post_dislike()), content_type='application/json')


# 댓글 좋아요
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def reply_likes(request, pk):
    reply = Reply.objects.get(id=pk)
    likes = LikeFunction(request, reply.reply_post.board_id, reply.reply_like, reply.reply_dislike)
    return HttpResponse(json.dumps(likes.post_like()), content_type='application/json')


# 댓글 싫어요
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def reply_dislikes(request, pk):
    reply = Reply.objects.get(id=pk)
    dislikes = LikeFunction(request, reply.reply_post.board_id, reply.reply_like, reply.reply_dislike)
    return HttpResponse(json.dumps(dislikes.post_dislike()), content_type='application/json')


# 추천 클래스
class LikeFunction:
    def __init__(self, request, board_id, like, dislike):
        self.request = request
        self.board_id = board_id
        self.like = like
        self.dislike = dislike

    def post_like(self):
        if not self.request.session.get('authUser'):
            context = {'result':'login'}
            return context
        else:
            board_type = self.board_id
            login_session = self.request.session.get('authUser')['like']

            if login_session == '중도' and board_type[0:3] == 'opp' or login_session == '중도' and board_type[0:3] == 'rul':
                context = {'result':'fail'}
                return context
            elif login_session == '진보' and board_type[0:3] == 'rul':
                context = {'result':'fail'}
                return context
            elif login_session == '보수' and board_type[0:3] == 'opp':
                context = {'result':'fail'}
                return context
            else:
                user = self.request.session.get('authUser')['nickname']
                if self.dislike.filter(nickname=user).exists():
                    self.dislike.remove(user)
                    self.like.add(user)
                elif self.like.filter(nickname=user).exists():  # 이미 좋아요를 누른 유저일 때
                    self.like.remove(user)  # like field에 현재 유저 추가
                else:  # 좋아요를 누르지 않은 유저일 때
                    self.like.add(user)  # like field에 현재 유저 추기
                context = {'result':'success', 'like_count': self.like.count(),
                           'dislike_count': self.dislike.count()}
                return context

    def post_dislike(self):
        if not self.request.session.get('authUser'):
            context = {'result': 'login'}
            return context
        else:
            board_type = self.board_id
            login_session = self.request.session.get('authUser')['like']

            if login_session == '중도' and board_type[
                                         0:3] == 'opp' or login_session == '중도' and board_type[
                                                                                    0:3] == 'rul':
                context = {'result': 'fail'}
                return context
            elif login_session == '진보' and board_type[0:3] == 'rul':
                context = {'result': 'fail'}
                return context
            elif login_session == '보수' and board_type[0:3] == 'opp':
                context = {'result': 'fail'}
                return context
            else:
                user = self.request.session.get('authUser')['nickname']
                if self.like.filter(nickname=user).exists():  # 이미 좋아요를 누른 유저일 때
                    self.like.remove(user)  # like field에 현재 유저 삭제
                    self.dislike.add(user)
                elif self.dislike.filter(nickname=user).exists():  # 이미 좋아요를 누른 유저일 때
                    self.dislike.remove(user)  # like field에 현재 유저 추가
                else:  # 좋아요를 누르지 않은 유저일 때
                    self.dislike.add(user)  # dislike field에 현재 유저 추가
                context = {'result': 'success', 'like_count': self.like.count(),
                           'dislike_count': self.dislike.count()}
                return context
