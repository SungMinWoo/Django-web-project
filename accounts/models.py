from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=20, null=False, unique=True)
    nickname = models.CharField(max_length=20, null=False, unique=True, primary_key=True)
    email = models.EmailField(max_length=200, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    like = models.CharField(max_length=2, null=False)
    like_date = models.CharField(max_length=20, null=True)
    joindate = models.DateTimeField(auto_now=True, null=False)
    terms_agree_date = models.CharField(max_length=20, null=True)
    privacy_agree_date = models.CharField(max_length=20, null=True)
    user_ip = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'User({self.user_id}, {self.nickname}, {self.email}, {self.terms_agree_date},' \
               f'{self.privacy_agree_date})'

    class Meta:
        db_table = 'user'
        verbose_name = '유저'
        verbose_name_plural = '유저'


class LeaveUser(models.Model):
    leave_id = models.CharField(max_length=20, null=False)
    leave_nick = models.CharField(max_length=20, null=False)
    leave_email = models.EmailField(max_length=200, null=False)
    leave_date = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return f'{self.leave_email}, {self.leave_nick}, {self.leave_date}'

    class Meta:
        db_table = 'leave_user'
        verbose_name = '탈퇴 유저'
        verbose_name_plural = '탈퇴 유저'


class EmailVerification(models.Model):
    temp_email = models.EmailField(max_length=200, null=False, unique=False)
    temp_number = models.CharField(max_length=10, null=False)
    temp_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.temp_email}, {self.temp_number}, {self.temp_date}'

    class Meta:
        db_table = 'email verification'
        verbose_name = '이메일 인증 테이블'
        verbose_name_plural = '임시 이메일 인증 테이블'