import telebot
from django.core.management.base import BaseCommand
from os import getenv

from user.models import User

TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        user_id_from_command = message.text.split()[1]
        if not User.objects.filter(pk=user_id_from_command).exists():
            bot.reply_to(message, "Ты не зарегистрирован в системе! Зарегистрируйся, чтобы подписаться на " "рассылку!")
            return
        user = User.objects.get(pk=user_id_from_command)
        if user.telegram_id:
            bot.reply_to(message, "Ты уже подписан на рассылку!")
            return
        user.telegram_id = user_id
        user.save()
        bot.reply_to(message, "Ты успешно подписался на рассылку!")
    except IndexError:
        bot.reply_to(message, "Для того, чтобы подписаться на рассылку, введи команду /start <id>")


class Command(BaseCommand):
    def __init__(self):
        super().__init__()

    def handle(self, *args, **options):
        bot.polling()
