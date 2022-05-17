from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from garage.models import Vehicles, Glasses, VehicleResource, GlassesResource
from tablib import Dataset

from garage.forms import VehicleForm, GlassForm, UserRegistrationForm, UserLoginForm


def index(request):
    cars = Vehicles.objects.all()
    return render(request, 'garage/show.html', {"cars": cars})


def add_new_vehicle(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VehicleForm()
    return render(request, 'garage/index.html', {'form': form})


def edit_vehicle(request, id):
    vehicle = Vehicles.objects.get(id=id)
    return render(request, 'garage/edit_vehicle.html', {'vehicle': vehicle})


def update_vehicle(request, id):
    vehicle = Vehicles.objects.get(id=id)
    form = VehicleForm(request.POST, instance=vehicle)
    if form.is_valid():
        form.save()
        return redirect('home')
    else:
        return render(request, 'garage/edit_vehicle.html', {'vehicle': vehicle, 'form': form})


def destroy_vehicle(request, id):
    vehicle = Vehicles.objects.get(id=id)
    vehicle.delete()
    return redirect('home')


def glasses(requset, id):
    glass = Glasses.objects.filter(g_model_id=id)
    model_id = id
    return render(requset, 'garage/show_glass.html', {'glasses': glass, 'modelid': model_id})


def add_new_glass(request, id):
    if request.method == "POST":
        form = GlassForm(request.POST, initial={'g_model': id})
        if form.is_valid():
            form.save()
            return redirect(f'/glasses/{id}')
    else:
        form = GlassForm(initial={'g_model': id})
        return render(request, 'garage/add_glass.html', {'form': form, 'modelid': id})


def edit_glass(request, id):
    glass = Glasses.objects.get(id=id)
    return render(request, 'garage/edit_glass.html', {'glass': glass})


def update_glass(request, id):
    glass = Glasses.objects.get(id=id)
    model_id = glass.g_model_id
    form = GlassForm(request.POST, instance=glass)
    if form.is_valid():
        form.save()
        return redirect(f'/glasses/{model_id}')
    else:
        return render(request, 'garage/edit_glass.html', {'glass': glass, 'form': form})


def glass_details(request, id):
    glass = Glasses.objects.get(id=id)
    return render(request, 'garage/glass_details.html', {'glass': glass})


def destroy_glass(request, id):
    glass = Glasses.objects.get(id=id)
    model_id = glass.g_model_id
    glass.delete()
    return redirect(f'/glasses/{model_id}')


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


def login_func(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user or None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request, 'Username or password is wrong')
            return redirect('login')
    else:
        user_form = UserLoginForm()

    return render(request, 'registration/login.html', {'user_form': user_form})


def logout_func(request):
    logout(request)
    return redirect("/")


def import_to_vehicles(request):
    if request.method == 'POST':
        vehicle_resource = VehicleResource()
        dataset = Dataset()
        try:
            new_vehicles = request.FILES['vehicle_file']

            imported_data = dataset.load(new_vehicles.read())
            result = vehicle_resource.import_data(imported_data, dry_run=True)

            if not result.has_errors():
                vehicle_resource.import_data(dataset, dry_run=False)
            else:
                messages.warning(request, 'Wrong or empty file!')
                return redirect('/')
        except:
            messages.warning(request, 'Wrong or empty file!')
            return redirect('/')

    return redirect('/')


def import_to_glasses(request, id):
    if request.method == 'POST':
        try:
            glasses_resource = GlassesResource()
            dataset = Dataset()
            new_vehicles = request.FILES['glasses_file']

            imported_data = dataset.load(new_vehicles.read())
            result = glasses_resource.import_data(imported_data, dry_run=True)

            if not result.has_errors():
                glasses_resource.import_data(dataset, dry_run=False)
            else:
                messages.warning(request, 'Wrong or empty file!')
                return redirect(f'/glasses/{id}')
        except:
            messages.warning(request, 'Wrong or empty file!')
            return redirect(f'/glasses/{id}')

    return redirect(f'/glasses/{id}')

