from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.result import AsyncResult

from scraper.tasks import create_task


@api_view(['GET', 'POST'])
def task(request):
    if request.method == 'POST':
        if "type" in request.data:
            category_name = request.data["type"]
            task = create_task.delay(category_name) # create celery task
            return Response({"message": "Create task", "task_id": task.id, "data": request.data})
        else:
            return Response({"message": "Error, not found 'type' in POST request"})
    if request.method == 'GET': # get task status
        if "task_id" in request.data:
            task_id = request.data["task_id"]
            task_result = AsyncResult(task_id)
            result = {
                "task_id": task_id,
                "task_status": task_result.status,
                "task_result": task_result.result
            }
            return Response(result)
        else:
            return Response({"message": "Error, not found 'task_id' in GET request"})