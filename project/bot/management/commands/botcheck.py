from django.core.management.base import BaseCommand
from bot import bot

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bot.start_bot()