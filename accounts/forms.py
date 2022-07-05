from django.contrib.auth.models import User
from django import forms
#
# from django.core.exceptions import NON_FIELD_ERRORS
# # 폼은 html에 태그인데 프론트에서 사용자의 입력을 받는 인터페이스
# # 장고의 폼 : HTML의 폼 역할, 데이터베이스에 저장할 내용을 형식, 제약조건을 결정하게됨
#
#
# class RegisterForm(forms.ModelForm):
#     CHOICES = [('L', '좌파'),
#                ('C', '중도'),
#                ('R', '우파')]
#     username = forms.CharField(label='아이디', widget=forms.TextInput)
#                                # error_messages={'unique':u'이미 사용중인 아이디입니다.'})
#     nickname = forms.CharField(label='닉네임', widget=forms.TextInput,
#                                error_messages={'unique': u'이미 사용중인 닉네임입니다.'})
#     like = forms.ChoiceField(label='정치성향', choices=CHOICES, widget=forms.RadioSelect)
#     email = forms.EmailField(label='이메일', widget=forms.EmailInput,
#                                error_messages={'unique': u'이미 사용중인 이메일입니다.'})
#     password = forms.CharField(label='비밀번호',
#                                widget=forms.PasswordInput)  # 비밀번호, widget의 저 값은 ***나오게하는 것
#     password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)  # 비밀번호 확인
#
#     class Meta:
#         model = User
#         fields = ['username', 'nickname', 'like', 'email']
#         # 입력 받을 form이 자동으로 생성
#
#     def clean_password2(self):
#         cd = self.cleaned_data # sql 인잭션을 해놓은 data
#         if cd['password'] != cd['password2']:
#             raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
#         return cd['password2']
#
#     def clean_username(self):
#         cd = self.cleaned_data
#         user = User.objects.get(username=['username'])
#         if cd['username'] == user:
#             raise forms.ValidationError("이미 있는 아이디 입니다.")
#         else:
#             return cd['username']
#
#     def clean_email(self):
#         cd = self.cleaned_data
#
#         return cd['email']
#
