from django.shortcuts import render, redirect
from .forms import UserAdminCreationForm


def register(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'registration/register.html', {'form': form})