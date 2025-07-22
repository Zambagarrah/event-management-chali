from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.contrib import messages
from .forms import SignUpForm

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            try:
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)
                messages.success(request, f'Account created successfully! You have been assigned the {role} role.')
                return redirect('login')
            except Exception as e:
                messages.error(request, 'Account created but role assignment failed. Please contact admin.')
                return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('login')
# Create your views here.
