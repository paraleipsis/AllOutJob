from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from subscription.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from django.contrib import messages

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'subscription/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Register successful')
        return render(request, 'subscription/register_done.html', {'new_user': new_user})
    return render(request, 'subscription/register.html', {'form': form})


def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.specialization = data['specialization']
                user.sub_on = data['sub_on']
                user.save()
                messages.success(request, 'Data saved')
                return redirect('subscription:update')
        form = UserUpdateForm(
            initial={
                'city': user.city,
                'specialization': user.specialization,
                'sub_on': user.sub_on
            })
        return render(request, 'subscription/update.html', {'form': form})

    else:
        return redirect('subscription:login')


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'User is deleted')
    return redirect('subscription:login')
