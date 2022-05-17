from django.db import models
from django.contrib.auth.models import AbstractUser
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class Vehicles(models.Model):
    v_number = models.PositiveIntegerField(unique=True, blank=False, verbose_name='Vehicle NUM')
    v_manufacture = models.CharField(max_length=30, unique=False, blank=False, verbose_name='Manufacture')
    v_model = models.CharField(max_length=50, blank=False, verbose_name='Model')
    v_left_side = models.BooleanField(default=False, verbose_name='Left side')
    v_right_side = models.BooleanField(default=False, verbose_name='Right side')
    v_face_side = models.BooleanField(default=False, verbose_name='Face side')
    v_back_side = models.BooleanField(default=False, verbose_name='Back side')
    v_note = models.TextField(blank=True, verbose_name='Notes')
    v_date_of_prod = models.DateField(blank=False, verbose_name='Date of prod.')

    def __str__(self):
        self.v_number = str(self.v_number)
        return self.v_number

    class Meta:
        db_table = "vehicles"
        verbose_name_plural = 'Vehicles'


class Glasses(models.Model):
    g_model = models.ForeignKey(Vehicles, on_delete=models.CASCADE, verbose_name='Auto ID')
    g_damage_type = models.CharField(max_length=255, blank=False, verbose_name='Type of damage')
    g_glass_num = models.PositiveIntegerField(blank=False, verbose_name='Glass number')
    g_damage_side = models.CharField(max_length=30, verbose_name='Damage side')
    g_nak = models.FloatField(default=0, verbose_name='NaK')
    g_mgk = models.FloatField(default=0, verbose_name='MsK')
    g_alk = models.FloatField(default=0, verbose_name='AlK')
    g_sik = models.FloatField(default=0, verbose_name='SiK')
    g_sk = models.FloatField(default=0, verbose_name='S K')
    g_cik = models.FloatField(default=0, verbose_name='CiK')
    g_kka = models.FloatField(default=0, verbose_name='KKA')
    g_kkb = models.FloatField(default=0, verbose_name='KKB')
    g_caka = models.FloatField(default=0, verbose_name='CaKA')
    g_cakb = models.FloatField(default=0, verbose_name='CaKB')
    g_tik = models.FloatField(default=0, verbose_name='TiK')
    g_crk = models.FloatField(default=0, verbose_name='CrK')
    g_mnk = models.FloatField(default=0, verbose_name='MsK')
    g_fek = models.FloatField(default=0, verbose_name='FeK')
    g_coka = models.FloatField(default=0, verbose_name='CoK')
    g_cuka = models.FloatField(default=0, verbose_name='CuKA')
    g_cukb = models.FloatField(default=0, verbose_name='CuKB')
    g_znka = models.FloatField(default=0, verbose_name='ZnKA')
    g_znkb = models.FloatField(default=0, verbose_name='ZnKB')
    g_srk = models.FloatField(default=0, verbose_name='SrK')
    json_data = models.JSONField(default=dict, verbose_name='JSON data')

    class Meta:
        db_table = "glasses"
        verbose_name_plural = 'Glasses'

    def __int__(self):
        return self.g_glass_num


class CustomUser(AbstractUser):
    is_viewer = models.BooleanField(default=True)
    is_editor = models.BooleanField(default=False)


class VehicleResource(resources.ModelResource):
    class Meta:
        model = Vehicles


class GlassesResource(resources.ModelResource):
    g_model = fields.Field(
        column_name='g_model',
        attribute='g_model',
        widget=ForeignKeyWidget(Vehicles, 'v_number'))

    class Meta:
        model = Glasses
        fields = ('id', 'g_damage_type', 'g_glass_num', 'g_damage_side',
                  'g_nak', 'g_mgk', 'g_alk', 'g_sik', 'g_sk', 'g_cik', 'g_kka',
                  'g_kkb', 'g_caka', 'g_cakb', 'g_tik', 'g_crk', 'g_mnk', 'g_fek',
                  'g_coka', 'g_cuka', 'g_cukb', 'g_znka', 'g_znkb', 'g_srk', 'g_model')

