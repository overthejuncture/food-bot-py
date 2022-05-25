import telebot
# import mysql.connector
import logging
import mariadb
import sys
# from mysql.connector import errorcode

# try:
#     cnx = mysql.connector.connect(host="127.0.0.1",user="root",passwd="secret",database="food_bot_py")
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("Something is wrong with your user name or password")

#     elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does not exists")

#     else:
#         print(err)

# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

try:
    cnx = mariadb.connect(host="mysql",
        user="root",
        password="secret",
        port=3306, 
        database="food_bot_py")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)



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

