import telebot, sys, emoji, logging, time 
from telebot import types
from telebot import apihelper

PROXY = 'socks4://13.76.80.165:1234'
apihelper.proxy = {'https': PROXY}

bot = telebot.TeleBot('1011156027:AAElJxSe9oD2-GNkMiBG5x8jEIQmFrJRZCY')

@bot.message_handler(commands=['start'])
def any_msg(message):

  keyboardmain = types.InlineKeyboardMarkup(row_width=1)
  first_button = types.InlineKeyboardButton(text="Базовая математика", callback_data="first")
  sec_button = types.InlineKeyboardButton(text="Профильная математика", callback_data="second")
  third_button = types.InlineKeyboardButton(text="Русский язык", callback_data="third")
#  fourth_button = types.InlineKeyboardButton(text="Физика", callback_data="fourth")

  keyboardmain.add(first_button, sec_button, third_button)
  bot.send_message(message.chat.id, "Привет, ты написал мне /start. Выбери предмет, по которому хочешь получить задание", reply_markup=keyboardmain)


@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
  vars = []
  for url in actual_subjects:                     #actual_subjects из файла "получение_заданий.py"
    var = choose_a_var(url)                       #choose_a_var() из файла "функции_для_парсинга.py"
    vars.append(var)
    variants = del_extra_list(vars)               #del_extra_list() из файла "функции_для_парсинга.py"

  if call.data == "first":
    time.sleep(3.5)
    mb_task, mb_answer = get_tasks(variants[0])   #get_tasks() из файла "получение_заданий.py"
    bot.send_message(call.message.chat.id, mb_task)
    @bot.message_handler(content_types=["text"])
    def answering(message):
      if message == mb_answer:
        bot.send_message(message.from_user.id, f'Молодец! Ты ответил верно :thumbs_up:. Правильный ответ: {mb_answer}')
      else:
        bot.send_message(message.from_user.id, emoji.emojize(f'Правильный ответ: {mb_answer}'))

  elif call.data == "second":
    time.sleep(3.5)
    mp_task, mp_answer = get_tasks(variants[1])
    bot.send_message(call.message.chat.id, mp_task)
    @bot.message_handler(content_types=["text"])
    def answering(message):
      if message == mp_answer:
        bot.send_message(message.from_user.id, f'Молодец! Ты ответил верно :thumbs_up:. Правильный ответ: {mp_answer}')
      else:
        bot.send_message(message.from_user.id, emoji.emojize(f'Правильный ответ: {mp_answer}'))

  elif call.data == "third":
    time.sleep(3.5)
    rus_task, rus_answer = get_tasks(variants[2])
    bot.send_message(call.message.chat.id, rus_task)
    @bot.message_handler(content_types=["text"])
    def answering(message):
      if message == rus_answer:
        bot.send_message(message.from_user.id, f'Молодец! Ты ответил верно :thumbs_up:. Правильный ответ: {rus_answer}')
      else:
        bot.send_message(message.from_user.id, emoji.emojize(f'Правильный ответ: {rus_answer}'))

bot.infinity_polling()
