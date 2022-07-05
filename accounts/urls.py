from django.urls import path
from .views import login, logout, register, check_value, register_terms, mypage, my_write, \
    my_reply, delete_account, send_email, check_number, find_account, find_pw

app_name = 'accounts'

urlpatterns = [
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('register', register, name='register'),
    path('register-terms', register_terms, name='register_terms'),
    path('register/api/check-value/', check_value, name='check_value'),
    path('api/check-value/', check_value, name='check_value'),
    path('api/send-email/', send_email, name='send_email'),
    path('api/check-number/', check_number, name='send_email'),
    path('api/find-pw/', find_pw, name='find_pw'),
    path('mypage', mypage, name='mypage'),
    path('mypage/my-write', my_write, name='my_write'),
    path('mypage/my-reply', my_reply, name='my_reply'),
    path('mypage/leave-poty', delete_account, name='leave_poty'),
    path('mypage/api/check-value/', check_value, name='check_value'),
    path('find-account', find_account, name='find_account'),

]
