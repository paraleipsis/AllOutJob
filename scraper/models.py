from django.db import models

class BaseTask(models.Model):
    """ Celery task info"""
    name = models.CharField(max_length=100)
    is_success = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BaseParsingResult(models.Model):
    """ Parsing result details"""
    task_id = models.ForeignKey(
        BaseTask,
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )
    data = models.TextField(blank=True)
    task_type = models.CharField(blank=True, max_length=64)
