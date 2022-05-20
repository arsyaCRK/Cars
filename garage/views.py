import traceback

import openpyxl_dictreader

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from tablib import Dataset

from garage.models import Vehicles, Glasses, VehicleResource
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


def vehicle_details(request, id):
    car = Vehicles.objects.get(id=id)
    return render(request, 'garage/vehicle_details.html', {'car': car})


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


def import_vector(request, id):
    if request.method == 'POST':
        try:
            xls_file = request.FILES['vector_file']
            json_vector = {'values': []}
            json_values = {}
            reader = openpyxl_dictreader.DictReader(xls_file)
            for rows in reader:
                json_vector['values'].clear()
                for row_id, row_value in rows.items():
                    if isinstance(row_id, int):
                        json_vector['values'].append(row_value)
                    else:
                        json_vector[row_id] = row_value

                json_values['values'] = json_vector['values']
                vehicle = Vehicles.objects.get(id=json_vector['sample_id'])
                print(vehicle)
                vehicle.json_data = json_values
                vehicle.save()
        except:
            print(traceback.format_exc())
            messages.warning(request, 'Wrong or empty file!')
            return redirect(f'/glasses/{id}')

        return redirect(f'/glasses/{id}')


def import_to_glasses(request, id):
    if request.method == 'POST':
        try:
            xls_file = request.FILES['glasses_file']
            json_data = {}
            reader = openpyxl_dictreader.DictReader(xls_file)
            for rows in reader:
                for row_id, row_value in rows.items():
                    json_data[row_id] = row_value

                vehicle = Vehicles.objects.get(v_number=json_data['g_model'])
                vehicle_id = vehicle.id

                data_to_db = Glasses.objects.create(id=json_data['id'], g_damage_type=json_data['g_damage_type'],
                                                    g_glass_num=json_data['g_glass_num'],
                                                    g_damage_side=json_data['g_damage_side'],
                                                    g_nak=json_data['g_nak'], g_mgk=json_data['g_mgk'],
                                                    g_alk=json_data['g_alk'], g_sik=json_data['g_sik'],
                                                    g_sk=json_data['g_sk'], g_cik=json_data['g_cik'],
                                                    g_kka=json_data['g_kka'], g_kkb=json_data['g_kkb'],
                                                    g_caka=json_data['g_caka'], g_cakb=json_data['g_cakb'],
                                                    g_tik=json_data['g_tik'], g_crk=json_data['g_crk'],
                                                    g_mnk=json_data['g_mnk'], g_fek=json_data['g_fek'],
                                                    g_coka=json_data['g_coka'], g_cuka=json_data['g_cuka'],
                                                    g_cukb=json_data['g_cukb'], g_znka=json_data['g_znka'],
                                                    g_znkb=json_data['g_znkb'], g_srk=json_data['g_srk'],
                                                    g_model_id=vehicle_id)

                data_to_db.save()
        except:
            messages.warning(request, 'Wrong or empty file!')
            return redirect(f'/glasses/{id}')

    return redirect(f'/glasses/{id}')
