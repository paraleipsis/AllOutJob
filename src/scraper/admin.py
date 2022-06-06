from django.contrib import admin
from .models import City, Specialization, Vacancy, Error, Url

admin.site.register(City)
admin.site.register(Specialization)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)
