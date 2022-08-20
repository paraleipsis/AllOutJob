import requests

from lxml import etree
from scraper.models import BaseTask, BaseParsingResult
from celery import shared_task, current_task


def parse_data(celery_task_id: str, category_name: str):
    new_task = BaseTask.objects.create(
        name=celery_task_id,
    )
    new_task.save()
    try:
        response = requests.get(
            f"https://books.toscrape.com/catalogue/category/books/{category_name}/"
        )
        if response.status_code == 200:
            tree = etree.HTML(response.content)
            results = tree.xpath("//article/h3/a")
            for cur in results:
                cur_parsing_res = BaseParsingResult.objects.create(
                    task_id=new_task,
                    data=cur.text,
                    task_type=category_name
                )
                cur_parsing_res.save()
    except Exception as e:
        print("Error: ", e)
    else:
        new_task.is_success = True
        new_task.save()


@shared_task()
def create_task(category_name):
    parse_data(current_task.request.id, category_name)
    return True