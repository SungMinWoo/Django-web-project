from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import User


class Board(models.Model):
    board_id = models.CharField(max_length=20, null=False, verbose_name='게시판 종류')
    post_title = models.CharField(max_length=255, null=False)
    post_content = models.TextField(verbose_name='내용')
    post_like = models.ManyToManyField(User, related_name='post_likes', blank=True)
    post_dislike = models.ManyToManyField(User, related_name='post_dislikes', blank=True)
    post_writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='post_writer', verbose_name="작성자", null=True)
    post_create = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    post_update = models.DateTimeField(null=True, blank=True, verbose_name="수정일")
    post_views = models.PositiveIntegerField(default=0, verbose_name='조회수') # 0보다 크거나 같은 정수를 저장하는 필드

    def __str__(self):
        return self.post_title

    class Meta:
        db_table = 'board'

    def get_absolute_url(self):
        return reverse('board:id', args=[self.board_id, self.id])


class Reply(models.Model):
    reply_post = models.ForeignKey(Board, on_delete=models.CASCADE, default='')
    reply_contents = models.TextField(max_length=1000, null=False)
    reply_like = models.ManyToManyField(User, related_name='reply_likes', blank=True)
    reply_dislike = models.ManyToManyField(User, related_name='reply_dislikes', blank=True)
    reply_writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply_writer', default='')
    reply_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True) #대댓글

    reply_create = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    reply_update = models.DateTimeField(null=True, blank=True, verbose_name="수정일")

    class Meta:
        db_table = 'board_reply'


class ReplyCascade(models.Model): # many to many field는 ondelete가 없어서 이렇게 지정해야함.
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    reply_writer = models.ForeignKey(User, on_delete=models.CASCADE)


class Report(models.Model):
    report_post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True, default='')
    report_reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, default='')
    report_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    report_reason = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=False)
    report_create = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    class Meta:
        db_table = 'report'