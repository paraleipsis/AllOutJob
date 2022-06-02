from django.apps import AppConfig


class ScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraper'
    verbose_name = "Application for collecting vacancies"
