from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'get_username', 'get_email', 'get_first_name', 'get_last_name', 'gender', 'education_status'
    )
    list_select_related = ('user',)
    readonly_fields = ('get_username', 'get_email', 'get_first_name', 'get_last_name')
    fieldsets = (
        (None, {
            'fields': ('get_username', 'get_email', 'get_first_name', 'get_last_name', 'gender', 'education_status')
        }),
    )

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'
