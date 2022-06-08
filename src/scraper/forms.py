from django import forms
from scraper.models import City, Specialization, Vacancy


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
        empty_label=None
    )


class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City',
        empty_label='Choose City'
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Specialization',
        empty_label='Choose Specialization'
    )

    url = forms.CharField(
        label='URL',
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    title = forms.CharField(
        label='Vacancy',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    company = forms.CharField(
        label='Company',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Vacancy
        fields = '__all__'
