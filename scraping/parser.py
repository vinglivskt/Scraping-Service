import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint

__all__ = ('hh', 'rabota', 'habr')

headers = [{'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 '
                          'Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]


def hh(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')

            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-work-experience'}).text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': href,
                                 'description': content, 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "page do not response"})
    return jobs, errors


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://rostov.rabota.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'r-serp'})

            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'r-serp__item r-serp__item_vacancy'})

                for div in div_list:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'}).text
                    company = 'No name'
                    logo = div.find('img')
                    if logo:
                        company = logo['alt']
                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "page do not response"})
    return jobs, errors


def habr(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://career.habr.com'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'section-group section-group--gap-medium'})
            # print(main_div)
            if main_div:
                div_list = main_div.find_all('div', attrs={'class': 'vacancy-card'})

                for div in div_list:
                    title = div.find('div', attrs={'class': 'vacancy-card__title'})
                    href = title.a['href']

                    content = div.find('div', attrs={'class': 'vacancy-card__meta'}).text
                    company = div.find('div', attrs={'class': 'vacancy-card__company-title'}).text

                    jobs.append({'title': title.text, 'url': domain + href,
                                 'description': content, 'company': company, 'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': "Div does not exists"})
        else:
            errors.append({'url': url, 'title': "page do not response"})
    return jobs, errors

# if __name__ == '__main__':
#     # url = 'https://rostov.hh.ru/search/vacancy?text=python&area=76'
#     # url = 'https://rostov.rabota.ru/vacancy/?query=python'
#     url = 'https://career.habr.com/vacancies/programmist_python'
#     # jobs, errors = rabota(url)
#     jobs, errors = habr(url)
#     h = codecs.open('../work.txt', 'w', 'utf-8')
#     # h = codecs.open('rabota.txt', 'w', 'utf-8')
#     h.write(str(jobs))
#     h.close()
