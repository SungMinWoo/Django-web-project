from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import F, Count
from django.contrib import messages
from ipware.ip import get_client_ip

from accounts.google_api.google_api import gmail_api

from django.conf import settings
from .models import User, EmailVerification, LeaveUser
from board.models import Reply, Board

from argon2 import PasswordHasher

from public_function.public_func import paginator_func
from public_function.decorator import login_required, block_ip
from public_function.public_data import BLOCK_TIME, IP


from random import randrange
from ratelimit.decorators import ratelimit

import datetime


@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def login(request):
    if request.session.get('authUser'):
        # 세션 확인하여 로그인 상태일때 로그인 시도 시
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'registration/login.html')

    elif request.method == 'POST':
        error_msg = {}
        user_id = request.POST['username']
        password = request.POST['password']
        try:
            request.POST['auto_login'] # 자동로그인 설정시
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # false가 유지
        except:
            pass

        try: # 비밀번호가 일치하지 않는다면
            user = User.objects.get(user_id=user_id)
            PasswordHasher().verify(user.password, password)
        except:
            error_msg['msg'] = '아이디 혹은 비밀번호가 일치하지 않습니다.'
            return render(request, 'registration/login.html', error_msg)

        client_ip, is_routable = get_client_ip(request) # 로그인 유저의 ip주소
        if client_ip is None:
            pass
        else:
            user.user_ip = client_ip
            user.save()

        if user.like == 'l':
            like = '진보'
        elif user.like == 'c':
            like = '중도'
        else:
            like = '보수'

        request.session['authUser'] = {'user_id':user.user_id, 'nickname':user.nickname,'like':like}  #세션 등록 후 id like 판별
        if request.POST.get('next') == False or request.POST.get('next') == '/accounts/register' \
                or request.POST.get('next') == '/accounts/mypage' \
                or request.GET.get('next') == '/search' \
                or not request.GET.get('next')\
                or request.POST.get('next') == '/accounts/register-terms': # 특정 페이지에서 로그인 시 접근 안되는 곳 계속 추가할 것
            return redirect('/')
        else:
            return HttpResponseRedirect(request.POST.get('next')) # 로그인하기 이전 페이지로 넘겨줌


@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def logout(request):
    del request.session['authUser'] #세션 삭제
    if request.GET.get('next') == '/accounts/mypage' \
            or request.GET.get('next') == '/search' \
            or '/board/board_write/' in request.GET.get('next') \
            or not request.GET.get('next'):
        return HttpResponseRedirect('/') # 특정 페이지에서 로그아웃 시 메인으로 이동
    else:
        return HttpResponseRedirect(request.GET.get('next')) # 로그아웃 하기 이전 페이지로 넘겨줌


# 이용약관 및 개인정보 처리방침 동의
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def register_terms(request): # 이용약관 동의 시간 저장하기
    if request.method == 'GET':
        term_service = Board.objects.get(id=24) # local 89
        privacy_policy = Board.objects.get(id=23) # local 90
        context = {
            'term_service':term_service.post_content,
            'privacy_policy':privacy_policy.post_content
        }
        return render(request, 'registration/register_terms.html', context)
    elif request.method == 'POST':
        agree = request.POST.get('agreeProv')
        request.session['terms'] = {'agree':agree}
        return redirect('/accounts/register')

# 회원가입
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def register(request):
    if request.session.get('authUser'):
        # 세션 확인하여 로그인 상태일때 로그인 시도 시
        err_msg = '로그아웃 후 이용해주시기 바랍니다.'
        return render(request,  'main_page/main_page.html', {'session_error':err_msg})
    elif request.session.get('terms'):
        if request.method == 'GET':
            return render(request, 'registration/register.html')
        elif request.method == 'POST':
            user_id = request.POST.get('user_id')
            nickname = request.POST.get('nickname')
            email = request.POST.get('email')
            like = request.POST.get('like')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if(user_id or nickname or email or like or password) == '': # 지금 프론트에서 하는중 유효성 검사해야됨
                return redirect('/accounts/register')
            elif password != password2:
                return redirect('/accounts/register')
            else:
                now = datetime.datetime.now()
                time = now.strftime('%Y-%m-%d %H:%M:%S')
                user = User(
                    user_id=user_id,
                    nickname=nickname,
                    password=PasswordHasher().hash(password),
                    email=email,
                    like=like,
                    like_date=time,
                    terms_agree_date=time,
                    privacy_agree_date=time,
                )
                user.save()
                del request.session['terms']  # 세션 삭제
            return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        return redirect('/accounts/register-terms')


# 회원정보 체크 및 회원가입시 중복체크
@block_ip
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def check_value(request):
    value = request.POST['value']
    if request.session.get('authUser'):
        user_id = request.session.get('authUser')['user_id'] # 세션에서 아이디 값 추출
        user_pw = User.objects.get(user_id=user_id) # 비밀번호 확인

    if request.POST['id'] == "email":
        if User.objects.filter(email=value).exists():
            try:
                send_email = request.POST['send_email']
                send_user_id = User.objects.get(email=value)
                gmail_api(value, f"귀하의 아이디는 [{send_user_id.user_id}]입니다. 본인이 아닐 경우 문의바랍니다.")
                user = 'exist'
            except:
                user = None
        else:
            if LeaveUser.objects.filter(leave_email=value).exists():
                user = 'ban'
            else:
                user = None
    elif request.POST['id'] == "user_id":
        if User.objects.filter(user_id=value).exists():
            user = 'exist'
        else:
            user = None
    elif request.POST['id'] == "nickname":
        if User.objects.filter(nickname=value).exists():
            user = 'exist'
        else:
            user = None
    elif request.POST['id'] == "password": # 회원 정보 수정에 사용
        try:
            PasswordHasher().verify(user_pw.password, value) # 정보 수정에서 이전 정보와 같으면
            user = 'pw_pass'
        except Exception as e:
            user = 'pw_no_pass'
    else:
        user = None

    result = {
        'result': 'success',
        'data': user,
    }

    return JsonResponse(result)


#회원 정보 수정
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def mypage(request):
    if not request.session.get('authUser'):
        # 세션 확인하여 로그인 상태일때 로그인 시도 시
        err_msg = '로그인 후 이용해주시기 바랍니다.'
        return render(request,  'main_page/main_page.html', {'session_error':err_msg})
    # 세션정보에 있는 아이디를 통해 유저 찾기
    else:
        user_id = request.session.get('authUser')['user_id']  # 로그인 세션에서 닉네임 체크
        user = User.objects.get(user_id=user_id)

    if request.method == 'GET':
        if user.like == 'l':
            like = '진보'
        elif user.like == 'c':
            like = '중도'
        else:
            like = '보수'

        user_info = {
            'user_id': user.user_id,
            'nickname': user.nickname,
            'email': user.email,
            'like': like,
            'like_date': user.like_date,
        }
        return render(request, 'mypage/my_page.html', {'user_info': user_info})

    elif request.method == 'POST':
        now = datetime.datetime.now()
        time = now.strftime('%Y-%m-%d %H:%M:%S')

        nickname = request.POST.get('nickname')
        like = request.POST.get('like')
        password = request.POST.get('password1')

        if like == user.like:
            if nickname == '' or password == '':
                if nickname == '':
                    User.objects.filter(user_id=user_id).update(password=PasswordHasher().hash(password))  # 업데이트하는 방법임
                elif password == '':
                    User.objects.filter(user_id=user_id).update(nickname=nickname)
            elif nickname != '' and password != '':
                User.objects.filter(user_id=user_id).update(nickname=nickname,
                                                            password=PasswordHasher().hash(password))
        else:
            if nickname == '' and password == '':
                User.objects.filter(user_id=user_id).update(like=like, like_date=time)
            elif nickname == '' or password == '':
                if nickname == '':
                    User.objects.filter(user_id=user_id).update(like=like, like_date=time,
                                                                password=PasswordHasher().hash(password))
                elif password == '':
                    User.objects.filter(user_id=user_id).update(nickname=nickname, like=like,
                                                                like_date=time)
            elif (nickname != '') and (password != ''):
                User.objects.filter(user_id=user_id).update(nickname=nickname, like=like,
                                                            like_date=time, password=PasswordHasher().hash(password))

        return redirect('/accounts/mypage')


# 내가 쓴 게시글 보기
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def my_write(request):
    nick = request.session.get('authUser')['nickname']
    user = User.objects.get(nickname=nick)
    board = Board.objects.filter(post_writer=user).annotate(reply_count=Count(F('reply')))[::-1]  # 역참조로 댓글 갯수 확인
    board_data = paginator_func(request, board)

    return render(request, 'mypage/my_write.html', {'board':board_data})


# 내가 쓴 댓글 보기
@block_ip
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def my_reply(request):
    nick = request.session.get('authUser')['nickname']
    user = User.objects.get(nickname=nick)
    reply = Reply.objects.filter(reply_writer=user)[::-1]
    reply_data = paginator_func(request, reply)

    return render(request, 'mypage/my_reply.html', {'reply':reply_data})


# 계정 삭제
@login_required
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def delete_account(request):
    if request.method == 'GET':
        return render(request, 'mypage/leave_poty.html')
    elif request.method == 'POST':
        if request.session.get('authUser'):
            nickname = request.session.get('authUser')['nickname']

            user = User.objects.get(nickname=nickname)

            leave = LeaveUser(
                leave_id=user.user_id,
                leave_nick=user.nickname,
                leave_email=user.email,
            )
            leave.save()
            del request.session['authUser']
            user.delete()
            return redirect('/')
        else:
            return False


# 인증번호 보내기
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def send_email(request):
    user_email = request.POST['email']
    random_number = randrange(100000, 1000000, 1)
    # random_number = '0000'
    if EmailVerification.objects.filter(temp_email=user_email).exists():
        user = EmailVerification.objects.get(temp_email=user_email)
        user.delete()

    temp_data = EmailVerification(
        temp_email=user_email,
        temp_number=random_number,
    )
    temp_data.save()
    send_text = f'인증번호는 {random_number}입니다. 본인이 아닐 경우 관리자에게 문의바랍니다.'
    gmail_api(user_email, send_text)

    result = {
        'result': 'success',
    }
    return JsonResponse(result)


# 인증 번호 확인
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def check_number(request):
    email = request.GET['email']
    number = request.GET['number']

    now = datetime.datetime.now()

    if EmailVerification.objects.filter(temp_email=email).exists():
        user = EmailVerification.objects.get(temp_email=email)
        # if now >= user.temp_date + datetime.timedelta(seconds=600):
        #     result = 'fail'
        # else:
        if user.temp_number == number:
            result = 'pass'
            user.delete()
        else:
            result = 'fail'
    else:
        result = 'fail'
    json_data = {
        'result': 'success',
        'data': result,
    }
    return JsonResponse(json_data)


# 아이디 찾기
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def find_account(request):
    if request.method == 'GET':
        return render(request, 'registration/find_account.html')
    elif request.method == 'POST':
        password = request.POST.get('password1')
        email = request.POST.get('hidden_text')

        change_pw = User.objects.get(email=email)
        change_pw.password = PasswordHasher().hash(password)
        change_pw.save()
        messages.info(request, '비밀번호 변경이 완료되었습니다.')
        return render(request, 'registration/find_account.html')


# 비밀번호 찾기
@ratelimit(key=IP, rate=BLOCK_TIME, block=True)
def find_pw(request):
    email = request.POST['email']
    id = request.POST['id']
    if User.objects.filter(email=email).exists():
        if User.objects.filter(email=email, user_id=id).exists():
            send_email(request)
            result = 'pass'
        else:
            result = 'fail'
    elif LeaveUser.objects.filter(leave_email=email).exists():
        result = 'ban'
    else:
        result = None

    json_data = {
        'result': 'success',
        'data': result,
    }
    return JsonResponse(json_data)
