from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from ..validators.custom_validators import AdancedValidator

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.TextField(max_length=12, null=False, blank=False, validators=[AdancedValidator.check_user_name, MinLengthValidator(6)])
    password = models.TextField(max_length=24, null=False, blank=False, validators=[AdancedValidator.check_password, MinLengthValidator(6)])
    login_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.user_id)