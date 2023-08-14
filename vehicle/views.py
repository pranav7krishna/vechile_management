from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout

from .models import Vehicle, UserRole
from .forms import VehicleForm


def base_view(request):
    return render(request, 'base.html')


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserRole.objects.create(user=user, role='user')  # Assign default role
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('vehicle_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def vehicle_list(request):
    user_role = request.user.userrole.role
    if user_role == 'superadmin':
        vehicles = Vehicle.objects.all()
    elif user_role == 'admin':
        vehicles = Vehicle.objects.exclude(vehicle_type='Two')
    else:
        vehicles = Vehicle.objects.filter(vehicle_type='Four')
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'vehicle_detail.html', {'vehicle': vehicle})


@login_required
def vehicle_create(request):
    user_role = request.user.userrole.role
    if user_role in ['superadmin', 'admin']:
        if request.method == 'POST':
            form = VehicleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('vehicle_list')
        else:
            form = VehicleForm()
        return render(request, 'vehicle_form.html', {'form': form})
    else:
        return redirect('vehicle_list')


@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    user_role = request.user.userrole.role
    if user_role in ['superadmin', 'admin'] and (user_role == 'superadmin' or vehicle.vehicle_type != 'Two'):
        if request.method == 'POST':
            form = VehicleForm(request.POST, instance=vehicle)
            if form.is_valid():
                form.save()
                return redirect('vehicle_list')
        else:
            form = VehicleForm(instance=vehicle)
        return render(request, 'vehicle_form.html', {'form': form})
    else:
        return redirect('vehicle_list')


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    user_role = request.user.userrole.role
    if user_role == 'superadmin':
        if request.method == 'POST':
            vehicle.delete()
            return redirect('vehicle_list')
        return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})
    else:
        return redirect('vehicle_list')


def custom_logout(request):
    logout(request)
    return redirect('vehicle_list')
