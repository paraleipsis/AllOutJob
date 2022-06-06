from django.shortcuts import render
from .forms import FindForm
from .run_scraper import *


def home_view(request):
    form = FindForm()

    return render(request, 'scraper/home.html', {'form': form})


def list_view(request):
    Vacancy.objects.all().delete()
    form = FindForm()
    city = request.GET.get('city')
    specialization = request.GET.get('specialization')

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    run(loop, str(city), str(specialization))

    qs = Vacancy.objects.all()

    return render(
        request,
        'scraper/list.html',
        {'object_list': qs, 'form': form}
    )
