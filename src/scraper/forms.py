from django import forms
from scraper.models import City, Specialization


class FindForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City',
        initial=City.objects.get(name='Иркутск'),
        empty_label=None
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        to_field_name='slug',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Specialization',
        initial=Specialization.objects.get(name='Python'),
        empty_label=None
    )
