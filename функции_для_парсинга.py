"""Программа пишется и запускается на колабе.
Здесь прописаны функции (кроме основной функции get_tasks()), которые используются при парсинге"

def parsing_href(code_pieces):
    _urls = []
    for code_piece in code_pieces:
        url_in_cp = code_piece.get_attribute('href')
        _url = {'href': url_in_cp}
        only_url = list(_url.values())
        _urls.append(only_url)
    return _urls

def choose_a_var(suburl):
    driver.get(suburl)
    variants = driver.find_elements_by_xpath("//span[@class='Col Col_gap-right_n']//a")
    var_urls = parsing_href(variants)
    chosen_var = random.choice(var_urls)
    return chosen_var

def del_extra_list(some_list): #предназначение функции: если изначально получается список а-ля [[elem1], [elem2]], то данная ф-я превращает такую дичь просто в [elem1, elem2]
    useful_list = []
    for smth_in_brackets in some_list:
        for actual_smth in smth_in_brackets:
            useful_list.append(actual_smth)
    return useful_list
