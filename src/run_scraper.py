from scraper.scrapers import *

scrapers = ((hh, 'https://irkutsk.hh.ru/search/vacancy?text=python&from=suggest_post&salary=&clusters=true&area=35&ored_clusters=true&enable_snippets=true'),
            (superjob, 'https://irkutsk.superjob.ru/vacancy/search/?keywords=python'),
            (gorodrabot, 'https://irkutsk.gorodrabot.ru/python'))

jobs_list, errors = [], []
for func, url in scrapers:
    j, e = func(url)
    jobs_list += j
    errors += e

h = open('jobs.txt', 'w', encoding='utf-8')
h.write(str(jobs_list))
h.close()
