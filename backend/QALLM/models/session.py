from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from .user import User

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    session_name = models.TextField(max_length=120, null=False, blank=False, default="Trò chuyện mới", validators=[MinLengthValidator(1)])
    context = models.TextField(max_length=4000, null=False, blank=False, default="", validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.session_id)