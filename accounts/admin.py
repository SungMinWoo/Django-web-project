from django.contrib import admin

from .models import User, LeaveUser, EmailVerification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('password',) # 숨기기

    list_display = [
        'user_id',
        'nickname',
        'email',
        'like',
        'joindate',
        'user_ip',
    ]
    list_display_links = ['nickname']

    search_fields = ['nickname']

    list_filter = ['joindate']

    def has_change_permission(self, request, obj=None): # 수정 못하게
        return False


@admin.register(LeaveUser)
class LeaveUserAdmin(admin.ModelAdmin):
    list_display = [
        'leave_email',
        'leave_id',
        'leave_date',
    ]
    list_display_links = ['leave_email']

    search_fields = ['leave_email']

    list_filter = ['leave_date']

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = [
        'temp_email',
        'temp_number',
    ]

    def has_change_permission(self, request, obj=None):
        return False