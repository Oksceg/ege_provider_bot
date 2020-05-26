from bs4 import BeautifulSoup 
import sys, random, requests, json, re, time
from telebot import types
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
driver.get("https://yandex.ru/tutor/ege/?")

#subjects = driver.find_elements_by_xpath("//div[@class='SubjectItem SubjectItem_cols_2']//a")
#sub_urls = parsing_href(subjects)
#actual_subjects = del_extra_list(sub_urls)
actual_subjects = ['https://yandex.ru/tutor/subject/?subject_id=1', 'https://yandex.ru/tutor/subject/?subject_id=2', 'https://yandex.ru/tutor/subject/?subject_id=3', 'https://yandex.ru/tutor/subject/?subject_id=4', 'https://yandex.ru/tutor/subject/?subject_id=5', 'https://yandex.ru/tutor/subject/?subject_id=6', 'https://yandex.ru/tutor/subject/?subject_id=7', 'https://yandex.ru/tutor/subject/?subject_id=8', 'https://yandex.ru/tutor/subject/?subject_id=9', 'https://yandex.ru/tutor/subject/?subject_id=10', 'https://yandex.ru/tutor/subject/?subject_id=11', 'https://yandex.ru/tutor/subject/?subject_id=12', 'https://yandex.ru/tutor/subject/?subject_id=13', 'https://yandex.ru/tutor/subject/?subject_id=14', 'https://yandex.ru/tutor/subject/?subject_id=15']

#закомментировали строчки 13-15, чтобы снизить нагрузку на парсинг

def get_tasks(variant): 
  domain = 'http://yandex.ru'
  task = {}
  r = requests.get(variant)
  if r.ok:
    soup = BeautifulSoup(r.content, 'lxml')
    scripts = soup.findAll('script')
    time.sleep(3)
    for script in scripts:
      if script.has_attr('nonce') and 'window.__INIT__' in script.text: 
        js = script.text.strip('window.__INIT__ = ')
        numb = re.findall('T\d+', js)
        numbs = list(set(numb))
        des = []
        an = []
        time.sleep(3.5)
        for elem in numbs:
          task_descript = json.loads(js)["initialState"]["entities"]["task"][elem]['description']
          task_answ = json.loads(js)["initialState"]["entities"]["task"][elem]['answer']['value']
          time.sleep(3)
          e = []
          for smth in task_descript:
            e.append(smth['value'])
          des.append(e)
          an.append(task_answ)
        a = []
        b = []
        for i in enumerate(des, 1):
          a.append(i)
          if 'Докажите, ' in i:
            del a[i]
          if 'сочинение' in i:
            del a[i]
        for ii in enumerate(an, 1):
          b.append(ii)
        task = random.choice(a)
        mytask = list(task)
        nomer = int()
        ch = int()
        ch = mytask[0]
        nomer = ch-1
        myanswer = b[nomer]
        ohmytas = mytask[1]
        ohmytask = ' '.join(ohmytas)
        ohmyanswer = myanswer[1] 
        if '\times' in ohmytask:                                    #http://hijos.ru/nabor-formul-v-latex/ 
          ohmytask = ohmytask.replace('\times', '×')
        if type(ohmyanswer) == 'list':
          ohmyanswer = del_extra_list(ohmyanswer) #del_extra_list() — функция из файла "функции_для_парсинга.py"
        if '$' in ohmytask:
          ohmytask = ohmytask.replace('$', '')
        if '^{\circ}' in ohmytask:
          ohmytask = ohmytask.replace('^{\circ}', '°')
        if '\left' in ohmytask:
          ohmytask = ohmytask.replace('\left', '')
        if '\right' in ohmytask:
          ohmytask = ohmytask.replace('\right', '')
        if '\sqrt' in ohmytask:
          ohmytask = ohmytask.replace('}', ')')
          ohmytask = ohmytask.replace('{', '(')
          ohmytask = ohmytask.replace('\sqrt', '√')
        if 'circ' in ohmytask:
          ohmytask = ohmytask.replace('^{\circ}', '°')
          ohmytask = ohmytask.replace('^\circ', '°')
        if 'frac' in ohmytask:
          ohmytask = ohmytask.replace('-\frac', '')
          ohmytask = ohmytask.replace('\frac', '')
          ohmytask = ohmytask.replace('}{', ')/(')
          ohmytask = ohmytask.replace('{', '(')
          ohmytask = ohmytask.replace('}', ')')
        if '\le' in ohmytask:
          ohmytask = ohmytask.replace('\le', '≤')
        if '\ge' in ohmytask:
          ohmytask = ohmytask.replace('\ge', '≥')
        if 'cdot' in ohmytask:
          ohmytask = ohmytask.replace('\cdot', '⋅')
        if '<br><br>' in ohmytask:
          ohmytask = ohmytask.replace('<br><br>', '\n')
        if '<b>' in ohmytask:
          ohmytask = ohmytask.replace('<b>', '')
        if '</b>' in ohmytask:
          ohmytask = ohmytask.replace('</b>', '')
        return ohmytask, ohmyanswer
