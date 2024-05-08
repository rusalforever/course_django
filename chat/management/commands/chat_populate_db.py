from django.core.management.base import BaseCommand
import random
from faker import Faker
from hr.models import Employee as User
from chat.models import Thread, Message

fake = Faker("uk_UA")


class Command(BaseCommand):
    help = "Populate database with test data"

    def handle(self, *args, **kwargs):
        self.create_fake_threads_and_messages(
            100, 100
        )  # Change the number of threads and messages per thread as needed

    def create_fake_threads_and_messages(self, num_threads, num_messages_per_thread):
        users = User.objects.all()
        for _ in range(num_threads):
            participant1 = random.choice(users)
            participant2 = random.choice(users.exclude(pk=participant1.pk))
            thread = Thread.objects.create()
            thread.participants.set([participant1, participant2])
            thread.save()
            for _ in range(num_messages_per_thread):
                sender = random.choice([participant1, participant2])
                text = fake.text()
                Message.objects.create(sender=sender, text=text, thread=thread)
