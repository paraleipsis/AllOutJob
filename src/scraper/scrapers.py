import requests
from bs4 import BeautifulSoup as bs
from random import randint

__all__ = ('hh', 'superjob', 'gorodrabot')

header = [{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
           {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}]


def hh(url):
    headers = header[randint(0, 2)]
    jobs_list = []
    errors = []
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')

        try:
            page_amount = int(soup.find_all('span', attrs={'class': 'pager-item-not-in-short-range'})[-1].text)+1
        except IndexError:
            page_amount = 1

        div_list = []
        for i in range(page_amount):
            resp = requests.get(f'{url}?page={i}', headers=headers)
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find(
                'div',
                id='a11y-main-content'
            )
            if main_div:
                div_list += main_div.find_all(
                    'div',
                    attrs={'class': 'vacancy-serp-item__layout'}
                )
            else:
                errors.append({'url': url, 'title': 'div does not exists'})

        for div in div_list:
            v_title = div.find('h3')
            v_link = v_title.a['href']
            try:
                v_desc_resp = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                v_desc_req = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
            except AttributeError:
                v_desc_resp = ''
                v_desc_req = 'без описания требований'
                continue
            company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text

            jobs_list.append({
                'title': v_title.text,
                'url': v_link,
                'description_resp': v_desc_resp,
                'description_req': v_desc_req,
                'company': company
            })
    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs_list, errors


def superjob(url):
    headers = header[randint(0, 2)]
    jobs_list = []
    errors = []
    domain = 'https://irkutsk.superjob.ru'
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')
        new_jobs = soup.find('div', attrs={'class': '_5isIP _1I9pQ _3K6CQ L6dwW'})
        page_amount = len(soup.find_all('span', attrs={'class': '_28Wuq KNGBZ _4N0O3 _3lqNe _27m6C _R43B'}))

        if not page_amount:
            page_amount = 1

        if not new_jobs:

            div_list = []
            for i in range(1, page_amount + 1):
                resp = requests.get(f'{url}&page={i}', headers=headers)
                soup = bs(resp.content, 'html.parser')
                main_div = soup.find(
                    'div',
                    attrs={'class': '_3igJl orZAI _2qMLS'}
                )
                if main_div:
                    div_list += main_div.find_all(
                        'div',
                        attrs={'class': 'f-test-search-result-item'}
                    )
                else:
                    errors.append({'url': url, 'title': 'div does not exists'})

            for div in div_list:

                try:
                    v_title = div.find('a')
                    v_link = domain + v_title['href']
                    v_desc_resp = div.find('span', attrs={'class': '_1AFgi _3OHir z4PWH _1flRt t0SHb _1aWAq'}).text
                    company = div.find('span', attrs={
                        'class': '_3nMqD f-test-text-vacancy-item-company-name _3OHir z4PWH _1flRt t0SHb _1aWAq'}).text
                except (TypeError, AttributeError):
                    continue

                jobs_list.append({
                    'title': v_title.text,
                    'url': v_link,
                    'description_resp': v_desc_resp[:130],
                    'description_req': v_desc_resp[131:],
                    'company': company
                })
        else:
            errors.append({'url': url, 'title': 'page is empty'})
    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs_list, errors


def gorodrabot(url):
    headers = header[randint(0, 2)]
    jobs_list = []
    errors = []
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
        soup = bs(resp.content, 'html.parser')
        page_amount = len(soup.find_all('li', attrs={'class': 'pager__item'}))-1

        if not page_amount:
            page_amount = 1

        div_list = []
        for i in range(1, page_amount+1):
            resp = requests.get(f'{url}?p={i}', headers=headers)
            soup = bs(resp.content, 'html.parser')
            main_div = soup.find(
                'div',
                attrs={'class': 'content__block content__module'}
            )
            if main_div:
                div_list += main_div.find_all(
                    'div',
                    attrs={'class': 'snippet__inner'}
                )
            else:
                errors.append({'url': url, 'title': 'div does not exists'})

        for div in div_list:
            v_title = div.find('h2')
            v_link = v_title.a['href']
            v_desc_resp = div.find('div', attrs={'class': 'snippet__desc'}).text
            v_desc_req = ''
            company = div.find('li', attrs={'class': 'snippet__meta-item snippet__meta-item_company'}).text

            jobs_list.append({
                'title': v_title.text,
                'url': v_link,
                'description_resp': v_desc_resp.strip(),
                'description_req': v_desc_req,
                'company': company.strip()
            })

    else:
        errors.append({'url': url, 'title': 'page do not response'})

    return jobs_list, errors

