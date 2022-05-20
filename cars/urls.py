from django.contrib import admin
from django.urls import path, re_path, include
from garage import views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('addnew', views.add_new_vehicle),
    path('edit/<int:id>', views.edit_vehicle),
    path('update/<int:id>', views.update_vehicle),
    path('destroy/<int:id>', views.destroy_vehicle),
    path('glasses/<int:id>', views.glasses),
    path('addnewglass/<int:id>', views.add_new_glass),
    path('editglass/<int:id>', views.edit_glass),
    path('updateglass/<int:id>', views.update_glass),
    path('destroyglass/<int:id>', views.destroy_glass),
    path('vehicledetails/<int:id>', views.vehicle_details),
    re_path(r'^login/$', views.login_func, name='login'),
    re_path(r'^logout/', views.logout_func, name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    path('importvehicles/', views.import_to_vehicles),
    path('glasses/importvector/<int:id>', views.import_vector),
    path('glasses/importglasses/<int:id>', views.import_to_glasses),
    path('', views.index, name='home'),
]
