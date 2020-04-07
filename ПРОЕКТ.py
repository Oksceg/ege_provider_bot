'''Программа пишется и запускается в колабе.
Часть 1: установка библиотек для работы с телеграмом, браузером, парсингом'''

!pip install pytelegrambotapi 
!pip install selenium 
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin

from bs4 import BeautifulSoup
import sys, telebot, random, requests, json
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get("https://yandex.ru/tutor/") #здесь уже приступаем к работе с указанной ссылкой (часть 2)

def get_href(things): #Название функции, возможно, поменяем, а в целом она является важной частю парсинга. Далее используется для создания списка из предметов ЕГЭ. 
    thing_urls = []
    for one_thing in things:
        one_thing_url = one_thing.get_attribute('href')
        thing_url = {'href': one_thing_url}
        only_url = list(thing_url.values())
        thing_urls.append(only_url)
    return thing_urls

def choose_a_var(suburl): #с помощью этой функции отбирается вариант
    driver.get(suburl)
    variants = driver.find_elements_by_xpath("//span[@class='Col Col_gap-right_n']//a")
    var_urls = get_href(variants)
    chosen_var = random.choice(var_urls)
    return chosen_var

def del_extra_list(some_list): #предназначение функции: если изначально получается список а-ля [[elem1], [elem2]], то данная ф-я превращает такую дичь просто в [elem1, elem2]
    useful_list = []
    for smth_in_brackets in some_list:
        for actual_smth in smth_in_brackets:
            useful_list.append(actual_smth)
    return useful_list


subjects = driver.find_elements_by_xpath("//div[@class='SubjectItem SubjectItem_cols_2']//a")
sub_urls = get_href(subjects)
actual_subjects = del_extra_list(sub_urls)
print("предметы: ", actual_subjects)
vars = []
for url in actual_subjects:
  var = choose_a_var(url)
  vars.append(var)
variants = del_extra_list(vars)
print("вар", variants[0])


def get_tasks(task_page_link):
    domain = 'http://yandex.ru'
    tasks = []
    r = requests.get(variants[0]) #под нулем идет матеша(база)
    if r.ok:
        soup = BeautifulSoup(r.content, 'lxml')
    scripts = soup.findAll('script')
    for script in scripts:
        if script.has_attr('nonce') and 'window.__INIT__' in script.text: #эта штука проверяет все найденные тэги script на наличие следующих аттрибутов (не знаю откуда мы это знаем но задания именно с этими аттрибутами)
            js = script.text.strip('window.__INIT__ = ')
 #           js.get_attribute('description') 
            print("json ", json.loads(js))
            tasks = tasks.append(json.loads(js))
    return tasks


tasks = get_tasks(variants[0])
print('задания', tasks) #выдает пустой список :(


def parse_task(task_html_source):
    task = {}

    
    for div in task_html_source.find_all('div'):
       
      if 'class' not in div.attrs:
          continue
      print(div.attrs['class']) 
      if 'HeaderTitle' in div.attrs['class']:
          task['id'] = 1
          task['id'] = (div
              .find("h3")
#                 .find("span", recursive=False)
#                 .find("span", recursive=False)
#                 .find("a", recursive=False)
#                 .find("span", recursive=False)
                .text
        )
#         if 'Task-Description' in div.attrs['class']:
#             task_description = 
#             tasks.append(div)
    return task

"""Часть 3 (пока что), работа непосредственно с ботом. 
Бот уже сейчас существует и даже на что-то отвечает, но здесь не будет происходить обновлений до того момента,
пока не будет осуществлян полный парсинг базовой математики"""

bot = telebot.TeleBot('') #здесь токен от бота

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start. Теперь выбери один или несколько предметов, по которым ты хочешь готовиться к ЕГЭ:\n/math_b - Математика (базовый уровень)\n/math_p - Математика (профильный уровень)')
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == '/math_b':
        bot.send_message(message.chat.id, 'Отлично! Держи задания по базовой математике: ')
    elif message.text == '/math_p':
        bot.send_message(message.chat.id, 'Отлично! Держи задания по профильной математике: ')
    elif message.text == 'Математика (профиль)':
        bot.send_message(message.chat.id, 'Отлично! Держи задания по профильной математике: ')
bot.polling()
