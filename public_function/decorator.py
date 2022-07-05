from django.http import HttpResponseForbidden
from django.shortcuts import redirect

ALLOWED_IP_BLOCKS = ['127.0.0.2']


# ip 차단
def block_ip(func):
    def wrap(request, *args, **kwargs):
        if request.META.get('REMOTE_ADDR') in ALLOWED_IP_BLOCKS:
            return HttpResponseForbidden('<h3>과도한 트레픽 유발을 이유로 사이트를 이용하실 수 없습니다.</h3><h6>자세한 사항은 문의바랍니다.</h6>')
        return func(request, *args, **kwargs)
    return wrap


# 로그인 확인
def login_required(func):
    def wrap(request, *args, **kwargs):
        login_session = request.session.get('authUser', '')
        if login_session == '':
            return redirect('accounts:login')
        return func(request, *args, **kwargs)
    return wrap
