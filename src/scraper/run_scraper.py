import asyncio
import os
import sys
import datetime as dt
import django
from django.db import DatabaseError
from scraper.scrapers import *

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "alloutjob.settings"

django.setup()

from scraper.models import Vacancy, Error


async def main(value, loop, jobs_list, errors):
    func, url = value
    job, err = await loop.run_in_executor(None, func, url)
    errors.extend(err)
    jobs_list.extend(job)


def run(loop, city, specialization):
    jobs_list, errors = [], []

    scrapers = ((hh,
                 f'https://{city}.hh.ru/search/vacancy?text={specialization}&from=suggest_post&salary=&clusters=true&area=35&ored_clusters=true&enable_snippets=true'),
                (superjob, f'https://{city}.superjob.ru/vacancy/search/?keywords={specialization}'),
                (gorodrabot, f'https://{city}.gorodrabot.ru/{specialization}'))

    tmp_task = [
        (func, url)
        for func, url in scrapers
    ]

    tasks = asyncio.wait([loop.create_task(main(f, loop, jobs_list, errors)) for f in tmp_task])
    loop.run_until_complete(tasks)
    loop.close()

    l = []
    for job in jobs_list:
        if str(job['title']).strip() not in l:
            l.append(str(job['title']).strip())
            v = Vacancy(**job)
            try:
                v.save()
            except DatabaseError:
                pass

    if errors:
        qs = Error.objects.filter(timestamp=dt.date.today())
        if qs.exists():
            err = qs.first()
            # err.data.update({'errors': errors})
            err.save()
        else:
            Error(data=f'errors:{errors}').save()
