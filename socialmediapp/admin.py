from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment, Like, CommentLike, Follow

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {'fields': ('profile_picture', 'bio', 'website', 'location')}),
    )

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_preview', 'created_at']
    list_filter = ['created_at', 'user']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'content_preview', 'created_at']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

admin.site.register(Like)
admin.site.register(CommentLike)
admin.site.register(Follow)