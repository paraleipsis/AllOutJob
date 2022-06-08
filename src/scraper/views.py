from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from .forms import FindForm, VForm
from .models import Vacancy


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


def v_detail(request, pk=None):
    object_ = get_object_or_404(Vacancy, pk=pk)
    return render(request, 'scraper/detail.html', {'object': object_})


class VDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scraper/detail.html'


class VList(ListView):
    model = Vacancy
    template_name = 'scraper/list.html'
    form = FindForm()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = self.request.GET.get('city')
        context['specialization'] = self.request.GET.get('specialization')
        context['form'] = self.form

        return context

    def get_queryset(self):
        city = self.request.GET.get('city')
        specialization = self.request.GET.get('specialization')
        qs = []
        if city or specialization:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if specialization:
                _filter['specialization__slug'] = specialization
            qs = Vacancy.objects.filter(**_filter).select_related('city', 'specialization')

        return qs


class VCreate(CreateView):
    model = Vacancy
    form_class = VForm
    template_name = 'scraper/create.html'
    success_url = reverse_lazy('home')


class VUpdate(UpdateView):
    model = Vacancy
    form_class = VForm
    template_name = 'scraper/create.html'
    success_url = reverse_lazy('home')


class VDelete(DeleteView):
    model = Vacancy
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Vacancy deleted')
        return self.post(request, *args, **kwargs)
