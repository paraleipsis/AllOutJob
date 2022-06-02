from django.db import models
from pytils.translit import slugify


class City(models.Model):
    name = models.CharField(max_length=50, 
                            verbose_name='City name',
                            unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)
    
    class Meta:
        verbose_name = "City name"
        verbose_name_plural = "City's names"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=150,
                            verbose_name='Specialization',
                            unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Specialization"
        verbose_name_plural = "Specializations"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255, verbose_name='Vacancy')
    company = models.CharField(max_length=255, verbose_name='Company')
    description = models.TextField(verbose_name='Vacancy description')
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name='City')
    specialization = models.ForeignKey('Specialization', on_delete=models.CASCADE, verbose_name='Specialization')

    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Vacancy"
        verbose_name_plural = "Vacancies"

    def __str__(self):
        return self.title
