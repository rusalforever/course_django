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


"""
from django.db.models import Count

# Отримання кількості повідомлень у кожному потоці
thread_message_counts = Thread.objects.annotate(message_count=Count('message'))

for thread in thread_message_counts:
    print(f"Thread ID: {thread.id}, Message Count: {thread.message_count}")
    
   
   
    
from django.db.models import Max

# Отримання останнього повідомлення у кожному потоці
latest_messages = Message.objects.values('thread_id').annotate(
    latest_message_time=Max('created')
)

for msg in latest_messages:
    latest_message = Message.objects.filter(
        thread_id=msg['thread_id'],
        created=msg['latest_message_time']
    ).first()
    print(f"Thread ID: {latest_message.thread_id}, Latest Message: {latest_message.text}")
    
    
    
# Отримання унікальних користувачів, які беруть участь у потоках
unique_users = User.objects.filter(thread__isnull=False).distinct()

for user in unique_users:
    print(f"User ID: {user.id}, Username: {user.username}")
    
    
    
from django.db.models import Count

# Отримання користувачів з найбільшою кількістю повідомлень у потоках
users_with_most_messages = User.objects.annotate(
    message_count=Count('message_sender')
).order_by('-message_count')[:5]  # Вибираємо перші 5 користувачів

for user in users_with_most_messages:
    print(f"User ID: {user.id}, Username: {user.username}, Message Count: {user.message_count}")
        

"""
