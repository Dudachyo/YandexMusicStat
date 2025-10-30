from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Profile'
    verbose_name_plural = 'Profile'
    fields = ['hidden','encrypted_token', 'bio',  'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)

# Регистрируем с CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'has_token_display','hidden', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']

    def has_token_display(self, obj):
        return obj.has_token()

    has_token_display.short_description = 'Have token'
    has_token_display.boolean = True