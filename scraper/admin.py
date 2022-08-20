from django.contrib import admin

from .models import BaseTask, BaseParsingResult


@admin.register(BaseTask)
class BaseTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_success', 'created_at']
    readonly_fields = ['created_at']
    list_filter = ['is_success']

@admin.register(BaseParsingResult)
class BaseResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'task_id', 'data', 'task_type']