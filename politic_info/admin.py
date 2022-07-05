from django.contrib import admin

# Register your models here.
from .models import Politic, Rating


@admin.register(Politic)
class PoliticAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'politic_slug',
        'poli_nm',
    ]
    prepopulated_fields = {'politic_slug':['poli_nm']}


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = [
        'rate_num',
        'politic',
        'user_nick',
    ]
    search_fields = ['user_nk']

    list_filter = ['politic']

    def has_change_permission(self, request, obj=None):
        return False

    @admin.display(ordering='user_nk__nickname', description='작성자')
    def user_nick(self, obj):
        return obj.user_nk.nickname