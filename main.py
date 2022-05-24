import telebot
import mysql.connector
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# Создаем экземпляр бота
bot = telebot.TeleBot('5324840661:AAFz8VR-ludW4212dz4GlXWNyjN6joXCxXQ')
# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )')
# Получение сообщений от юзера
@bot.message_handler(commands=["list"])
def handle_text(message):
    bot.send_message(message.chat.id, '132')
# Запускаем бота
bot.polling(non_stop=True, interval=0)

