from django.contrib import admin
from .models import user, session, chat

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'password', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user_id', 'user_name']

class SessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user_id', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']
    search_fields = ['session_id', 'user_id']

class ChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'session_id', 'chat_position', 'user_ask', 'bot_answer', 'created_at', 'updated_at')
    list_filter = ['created_at', 'updated_at']
    search_fields = ['chat_id', 'session_id', 'chat_position', 'user_ask', 'bot_answer']

admin.site.register(user.User, UserAdmin)
admin.site.register(session.Session, SessionAdmin)
admin.site.register(chat.Chat, ChatAdmin)