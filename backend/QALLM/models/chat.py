from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MinValueValidator
from .session import Session

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=False, blank=False)
    chat_position = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1)])
    user_ask = models.TextField(max_length=4000, null=False, blank=False, validators=[MinLengthValidator(1)])
    bot_answer = models.TextField(max_length=4000, null=False, blank=False, validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.chat_id)