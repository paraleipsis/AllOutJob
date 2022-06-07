import os
import sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from alloutjob.settings import (
    EMAIL_HOST_USER,
    EMAIL_HOST,
    EMAIL_HOST_PASSWORD
)

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "alloutjob.settings"

django.setup()
from scraper.models import Vacancy, Error, Url

today = datetime.date.today()
subject = f"Vacancies for {today}"
text_content = f"Vacancies for {today}"
from_email = EMAIL_HOST_USER
empty = '<h2>There are no new vacancies</h2>'
User = get_user_model()

qs = User.objects.filter(sub_on=True).values('city', 'specialization', 'email')
users_dct = {}

for i in qs:
    users_dct.setdefault((i['city'], i['specialization']), [])
    users_dct[(i['city'], i['specialization'])].append(i['email'])
if users_dct:
    params = {'city_id__in': [], 'specialization_id__in': []}
    for pair in users_dct.keys():
        params['city_id__in'].append(pair[0])
        params['specialization_id__in'].append(pair[1])
    qs = Vacancy.objects.filter(**params, timestamp=today).values()
    vac = {}
    for i in qs:
        vac.setdefault((i['city_id'], i['specialization_id']), [])
        vac[(i['city_id'], i['specialization_id'])].append(i)
    for keys, emails in users_dct.items():
        rows = vac.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h3"><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p>{row["description"]} </p>'
            html += f'<p>{row["company"]} </p><br><hr>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
_html = ''
to = EMAIL_HOST_USER
if qs.exists():
    error = qs.first()
    data = error.data.get('errors', [])
    for i in data:
        _html += f'<p"><a href="{i["url"]}">Error: {i["title"]}</a></p><br>'
    subject = f'Scraping errors for {today}'
    text_content = 'Scraping errors'


qs = Url.objects.all().values('city', 'specialization')
urls_dct = {(i['city'], i['specialization']): True for i in qs}
urls_errors = ''
for keys in users_dct.keys():
    if keys not in urls_dct:
        urls_errors += f'<p">For City: {keys[0]} and Specialization: {keys[1]} URLs not found</p><br>'

if urls_errors:
    subject += 'URLs not found'
    _html += urls_errors

if subject:
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(_html, "text/html")
    msg.send()
