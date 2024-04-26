from django.core.exceptions import ValidationError
from django.db import models

# from django.contrib.auth.models import User
from hr.models import Employee as User


class Thread(models.Model):
    participants = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.participants.count() > 2:
            raise ValidationError("A Thread can't have more than 2 participants.")
        super().clean()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


