from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Board, Reply, Report


@admin.register(Board)
class BoardAdmin(SummernoteModelAdmin):
    summernote_fields = ('post_content',)
    search_fields = ['post_title', 'board_id', 'post_writer__nickname']
    list_display = (
        'id',
        'post_title',
        'writer_nick',
        'board_id',
        'post_views',
        'post_create',
        'post_update',
    )
    list_display_links = list_display
    list_filter = ['board_id']

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(ordering='post_writer__nickname', description='작성자')
    def writer_nick(self, obj):
        try:
            return obj.post_writer.nickname
        except:
            return None


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    search_fields = ['reply_writer__nickname', 'reply_contents']
    list_display = (
        'reply_contents',
        'writer_nick',
        'reply_create',
        'reply_update',
    )
    list_display_links = list_display
    list_filter = ['reply_post__board_id']

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(ordering='reply_writer__nickname', description='작성자')
    def writer_nick(self, obj):
        return obj.reply_writer.nickname


@admin.register(Report)
class ReplyAdmin(admin.ModelAdmin):
    search_fields = ['report_post__post_title', 'report_reply__reply_contents', 'report_user__nickname']
    list_display = (
        'writer_nick',
        'report_post',
        'report_reply',
        'report_reason',
        'report_create',
    )
    list_display_links = list_display
    list_filter = ['report_post__board_id']

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(ordering='reply_writer__nickname', description='작성자')
    def writer_nick(self, obj):
        return obj.reply_writer.nickname
