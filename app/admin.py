from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from app.models import Article

User = get_user_model()


@admin.decorators.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.decorators.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title')
