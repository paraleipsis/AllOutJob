from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraper.models import City, Specialization

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('no such user')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('wrong password')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('account is not available')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(
        label='Input email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Input password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError("passwords don't match")
        return data['password']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='City',
        initial=City.objects.get(name='Иркутск'),
        empty_label=None
    )

    specialization = forms.ModelChoiceField(
        queryset=Specialization.objects.all(),
        to_field_name='slug',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Specialization',
        initial=Specialization.objects.get(name='Python'),
        empty_label=None
    )

    sub_on = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput,
        label='Receive new vacancies on email'
    )

    class Meta:
        model = User
        fields = ('city', 'specialization', 'sub_on')
