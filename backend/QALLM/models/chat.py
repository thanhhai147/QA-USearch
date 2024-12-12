from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MinValueValidator
from .session import Session

MODEL_CHOICES = [
    ('gemini-1.5-pro', 'gemini-1.5-pro'),
    ('gpt-4.o-mini', 'gpt-4.o-mini'),
    ('llama-3.2-3b-instruct', 'llama-3.2-3b-instruct'),
]

PROMPTING_CHOICES = [
    ('zero-shot', 'zero-shot'),
    ('one-shot', 'one-shot'),
    ('few-shot', 'few-shot'),
    ('chai-of-thought', 'chain-of-thought')
]

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, null=False, blank=False)
    model = models.TextField(null=False, blank=False, choices=MODEL_CHOICES, default='gemini-1.5-pro')
    prompting = models.TextField(null=False, blank=False, choices=PROMPTING_CHOICES, default='zero-shot')
    chat_position = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1)])
    user_ask = models.TextField(max_length=4000, null=False, blank=False, validators=[MinLengthValidator(1)])
    bot_answer = models.TextField(max_length=4000, null=False, blank=False, validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.chat_id)