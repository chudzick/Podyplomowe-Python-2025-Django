from django.shortcuts import render, redirect
from .forms import RegisterForm


# Create your views here.
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'members/register.html', {
            'form': form
        })

    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.username = user.username.lower()
        user.save()
        return redirect('login')
    else:
        return render(request, 'members/register.html', {
            'form': form
        })
