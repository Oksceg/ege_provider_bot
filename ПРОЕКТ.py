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

"""Часть (?): в эфире эээксперименты! Что происходит: 
мы преобразовали функцию get_tasks в отдельный код, чтобы наблюдать за работой толькой этой части
Я даже решила вставить сюда два варианта этого кода(WARNING: используются регулярные выражения!)"""

#1) здесь ничего не просходит, но зато появляется json
from bs4 import BeautifulSoup
import sys, telebot, random, requests, json, re
domain = 'http://yandex.ru'
tasks = []
zadan = []
r = requests.get('https://yandex.ru/tutor/subject/variant/?subject_id=1&variant_id=338') #под нулем идет матеша(база)
if r.ok:
    soup = BeautifulSoup(r.content, 'lxml')
    scripts = soup.findAll('script')
    for script in scripts:
      if script.has_attr('nonce') and 'window.__INIT__' in script.text: #эта штука проверяет все найденные тэги script на наличие следующих аттрибутов (не знаю откуда мы это знаем но задания именно с этими аттрибутами)
         js = script.text.strip('window.__INIT__ = ')
         zadan = re.findall("'description'", js)
         print(zadan)
         print("jsn: ", json.loads(js))
#Если что, я имела в виду, что появляется это --> jsn:  {'path': 'tutor/subject/variant/', 'reqid': '1586453965032624-1049922972336434540366527-sas1-4556-sas-shared-app-host-14146', 'uri': '/tutor/subject/variant/?subject_id=1&variant_id=338', 'csrfToken': 'qU52pMHgrOBNJ82JpBwGkEe81lQ=:1586453965', 'region': '87', 'scriptsNonce': 'sqfqm', 'initialState': {'entities': {'scoremeterSubject': {'1': {'name': 'Математика (базовый уровень)', 'id': 1}}, 'task': {'T8339': {'subjectId': 1, 'breadCrumbsTitle': '1. Задание #T8339', 'modify_timestamp': 1566488817, 'partial_title': '1. Задание', 'author': {'name': '«СтатГрад»', 'html': 'Это задание составили эксперты <a href="https://statgrad.org" target="_blank">«СтатГрада»</a> для Яндекса', 'img': '', 'id': 3}, 'egeNumber': 1, 'id': 'T8339', 'egeNumberId': 81, 'solution': [{'caption': 'Указание:', 'type': 'text', 'value': 'Вспомните правила выполнения арифметических действий с обыкновенными, десятичными дробями и с отрицательными числами.', 'is_inline': None}, {'caption': 'Решение:', 'type': 'text', 'value': '$\\frac{2}{17}:\\left(-\\frac{5}{34}\\right)-2,8=-\\frac{2\\cdot34}{17\\cdot5}-2,8=-\\frac{4}{5}-2,8=-(0,8+2,8)=-3,6.$', 'is_inline': None}], '_link': '/tutor/subject/problem/?problem_id=T8339', 'topicId': 1, 'immediateCheck': 0, 'integer_id': 8339, 'answer': {'value': '-3,6', 'type': 'number'}, 'description': [{'caption': None, 'type': 'text', 'value': 'Найдите значение выражения $\\frac{2}{17}:\\left(-\\frac{5}{34}\\right)-2,8.$', 'is_inline': None}], 'reportMistake': 0, 'prototypeId': '', 'isAvailableForUserVariants': 0}, 'T8340': {'subjectId': 1, 'breadCrumbsTitle': '2. Задание #T8340', 'modify_timestamp': 1566488818, 'partial_title': '2. Задание', 'author': {'name': '«СтатГрад»', 'html': 'Это задание составили эксперты <a href="https://statgrad.org" target="_blank">«СтатГрада»</a> для Яндекса', 'img': '', 'id': 3}, 'egeNumber': 2, 'id': 'T8340', 'egeNumberId': 59, 'solution': [{'caption': 'Указание:', 'type': 'text', 'value': 'Используйте правила действий со степенями с одинаковым\nоснованием.', 'is_inline': None}, {'caption': 'Решение:', 'type': 'text', 'value': '$\\frac{6^{12}}{2^{9}\\cdot3^{11}}=\\frac{(2\\cdot3)^{12}}{2^{9}\\cdot3^{11}}=\\frac{2^{12}\\cdot3^{12}}{2^{9}\\cdot3^{11}}=\\frac{2^{3}\\cdot3}{1}=24.$', 'is_inline': None}], '_link': '/tutor/subject/problem/?problem_id=T8340', 'topicId': 2, 'immediateCheck': 0, 'integer_id': 8340, 'answer': {'value': 24, 'type': 'number'}, 'description': [{'caption': None, 'type': 'text', 'value': 'Найдите значение выражения $\\frac{6^{12}}{2^{9}\\cdot3^{11}}.$', 'is_inline': None}], 'reportMistake': 0, 'prototypeId': '', 'isAvailableForUserVariants': 0}, 'T8341': {'subjectId': 1, 'breadCrumbsTitle': '3. Задание #T8341', 'modify_timestamp': 1566488818, 'partial_title': '3. Задание', 'author': {'name': '«СтатГрад»', 'html': 'Это задание составили эксперты <a href="https://statgrad.org" target="_blank">«СтатГрада»</a> для Яндекса', 'img': '', 'id': 3}, 'egeNumber': 3, 'id': 'T8341', 'egeNumberId': 235, 'solution': [{'caption': 'Указание', 'type': 'text', 'value': 'Составьте пропорцию.', 'is_inline': None}, {'caption': 'Решение', 'type': 'text', 'value': '$250$ руб. — $100\\%,$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$x$ руб. — $2\\%;$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$\\frac{250}{x}=\\frac{100}{2};$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$x=\\frac{250\\cdot2}{100};$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$x=5;$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$250+5=255$ (руб.).', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': 'Возможны другие способы решения.\n', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$1.$\tЕжемесячная плата увеличится на $250\\cdot0,02=5$ рублей и в следующем году составит $250+5=255$ рублей.', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$2.$\tТак как ежемесячная плата увеличилась на $2\\%,$ она составит $250\\cdot1,02=255$рублей.', 'is_inline': None}], '_link': '/tutor/subject/problem/?problem_id=T8341', 'topicId': 3, 'immediateCheck': 0, 'integer_id': 8341, 'answer': {'value': 255, 'type': 'number'}, 'description': [{'caption': None, 'type': 'text', 'value': 'Ежемесячная плата за телефон составляет $250$ рублей. В следующем году она увеличится на $2\\%.$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': 'Сколько рублей будет составлять ежемесячная плата за телефон в следующем году?', 'is_inline': None}], 'reportMistake': 0, 'prototypeId': '', 'isAvailableForUserVariants': 0}, 'T8342': {'subjectId': 1, 'breadCrumbsTitle': '4. Задание #T8342', 'modify_timestamp': 1566488819, 'partial_title': '4. Задание', 'author': {'name': '«СтатГрад»', 'html': 'Это задание составили эксперты <a href="https://statgrad.org" target="_blank">«СтатГрада»</a> для Яндекса', 'img': '', 'id': 3}, 'egeNumber': 4, 'id': 'T8342', 'egeNumberId': 245, 'solution': [{'caption': 'Указание.', 'type': 'text', 'value': 'Выразите сопротивление $R$ из формулы $P=I^2R.$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': 'Подставьте значения переменных в формулу.', 'is_inline': None}, {'caption': 'Решение.', 'type': 'text', 'value': '$P=I^2R;$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$R=\\frac{P}{I^2};$', 'is_inline': None}, {'caption': None, 'type': 'text', 'value': '$R=\\frac{144}{4^2}=\\frac{144}{16}=9.$', 'is_inline': None}, и т.д там еще много
#и пустой список тоже

'''2) А вот здесь уже мы пытаемся осуществить попытку вытащить то, что идет рядом с value
(пример из jsn: ......[{'caption': 'Указание:', 'type': 'text', 'value': 'Вспомните правила выполнения арифметических действий с обыкновенными, десятичными дробями и с отрицательными числами.'......
тут уже выдает ошибку, а (jsn:) не печатается тоже'''
from bs4 import BeautifulSoup #в этом варианте кода появляется ошибка
import sys, telebot, random, requests, json, re
domain = 'http://yandex.ru'
tasks = []
zadan = []
r = requests.get('https://yandex.ru/tutor/subject/variant/?subject_id=1&variant_id=338') #под нулем идет матеша(база)
if r.ok:
    soup = BeautifulSoup(r.content, 'lxml')
    scripts = soup.findAll('script')
    for script in scripts:
      if script.has_attr('nonce') and 'window.__INIT__' in script.text: #эта штука проверяет все найденные тэги script на наличие следующих аттрибутов (не знаю откуда мы это знаем но задания именно с этими аттрибутами)
         js = script.text.strip('window.__INIT__ = ')
         pattern = "\'value\': \'[-0-9+=:.,А-Яа-я\\A-Za-z$\/{}()_ ]+\'"
         zadan = re.findall(pattern, js)
         print(zadan)
         print("jsn ", json.loads(js))
