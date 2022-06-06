from django.contrib import admin
from .models import City, Specialization, Vacancy, Error

admin.site.register(City)
admin.site.register(Specialization)
admin.site.register(Vacancy)
admin.site.register(Error)
