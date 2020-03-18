import telebot #pip install pytelegrambotapi - библиотека для телеги, далее следует обращаться к BotFather
bot = telebot.TeleBot('1011156027:AAElJxSe9oD2-GNkMiBG5x8jEIQmFrJRZCY')
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')
bot.polling()
