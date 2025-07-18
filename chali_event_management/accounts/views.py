from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            group = Group.objects.get(name=role)
            user.groups.add(group)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})
# Create your views here.
