from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    qs = []
    if city or specialization:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if specialization:
            _filter['specialization__slug'] = specialization

        qs = Vacancy.objects.filter(**_filter)
    return render(
        request,
        'scraper/home.html',
        {'object_list': qs, 'form': form}
    )
