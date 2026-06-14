from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Article

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'role', 'email', 'is_staff')
    list_filter = ('role', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role',)}),
    )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'published_at')
    list_filter = ('status', 'author')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'published_at')