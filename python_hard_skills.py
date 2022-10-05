import requests
from bs4 import BeautifulSoup
from collections import Counter
import re
import time
start_time = time.time()




ITEMS = 100
URL = f'https://rostov.hh.ru/search/vacancy?st=searchVacancy&text=python&items_on_page={ITEMS}'
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

def get_html(link):
    r = requests.get(link, headers=user_agent, timeout=5)
    return r.text


def extract_max_page():
  hh_requests = requests.get(URL, headers=user_agent, timeout=5)
  hh_soup = BeautifulSoup(hh_requests.text, 'lxml')
  pages = []
  paginator = hh_soup.find_all("span", {'class': 'pager-item-not-in-short-range'})
  for page in paginator:
    pages.append(int(page.find('a').text))
  return pages[-1]


def write_csv(data):
    with open('hhsave.csv', encoding='utf-8', mode='w') as f:
        for key, value in data.items():
            f.write(f'{key}, {value}\n')
    return


def comma(counter):
    old_dic = dict(counter)
    pattern = re.compile(r'\w+\s+\d+,')
    new_dic = {}
    for k, v in old_dic.items():
        if k.find(','):
            new_key = k.replace(',', '/')
            new_dic.update({new_key: v})
        else:
            new_dic.update({k: v})
    return new_dic


def get_ks(html):
    soup = BeautifulSoup(html, 'lxml')
    ks = []
    key = soup.find_all('div', class_='bloko-tag bloko-tag_inline')
    for k in key:
        ks.append(k.find('span', class_='bloko-tag__section bloko-tag__section_text').text.strip().replace('\xa0', ' '))
    return ks


def main():
    max_page = extract_max_page()
    extract_jobs(max_page)


def extract_jobs(last_page):
    keys = []
    for page in range(last_page):
        print(f'Парсинг страницы {page}')
        result = requests.get(f'{URL}&page={page}', headers=user_agent)
        soup = BeautifulSoup(result.text, 'lxml')
        results = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})
        for result in results:
            name = result.find('a').text
            if re.search(r'(?i)python', name, re.IGNORECASE):
                link = result.find('a')['href']
                keys.extend(get_ks(get_html(link)))
    cnt = Counter(keys)
    cnt = comma(cnt)
    write_csv(cnt)
    return


if __name__ == '__main__':
    main()


def convertsec(sec):
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    min = sec // 60
    sec %= 60
    return "%02d:%02d:%02d" % (hour, min, sec)

sec = time.time() - start_time
print("Total script running time :-", convertsec(sec))