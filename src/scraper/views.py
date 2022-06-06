from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import FindForm
from .models import Vacancy, City


def home_view(request):
    form = FindForm()
    return render(request, 'scraper/home.html', {'form': form})


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')
    context = {'city': city, 'specialization': specialization, 'form': form}

    if city or specialization:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if specialization:
            _filter['specialization__slug'] = specialization

        qs = Vacancy.objects.filter(**_filter).select_related('city', 'specialization')

        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['object_list'] = page_obj

    return render(
        request,
        'scraper/list.html',
        context
    )
