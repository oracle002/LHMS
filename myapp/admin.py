from django.contrib import admin
from myapp.models import Disease
from myapp.models import Vaccines
from myapp.models import Farmer
from myapp.models import Cattle
from myapp.models import Vaccination_Reg,Vaccination_S,ArtificialInsemination,Bull
# Register your models here.\

from django.contrib import admin
from .models import Vaccines, Disease, Farmer, Cattle

class VaccinesAdmin(admin.ModelAdmin):
    list_display = ('vaccine', 'catagory')
    search_fields = ('vaccine', 'catagory')

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('disease', 'vaccine', 'firstdose', 'boosterdose', 'subsequentdose')
    search_fields = ('disease', 'vaccine__vaccine')

class FarmerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phonenumber', 'addressline1', 'addressline2', 'place', 'pin')
    search_fields = ('firstname', 'lastname', 'email', 'phonenumber', 'place', 'pin')

class CattleAdmin(admin.ModelAdmin):
    list_display = ('tagno', 'breed', 'gender','dob','age_years', 'age', 'weight', 'color', 'owner')
    search_fields = ('tagno', 'breed', 'gender', 'color', 'owner__firstname', 'owner__lastname', 'owner__email')
    list_filter = ('owner', 'dob', 'age', 'age_years')


class Vaccination_RegAdmin(admin.ModelAdmin):
    list_display = ('cattleid', 'farmerid', 'diseaseid', 'vaccine', 'date_requested', 'date_approved', 'dose', 'status')
    list_filter = ('status', 'dose', 'date_requested', 'date_approved')
    search_fields = ('cattleid__tagno', 'farmerid__firstname', 'farmerid__lastname', 'disease', 'vaccine')

class Vaccination_SAdmin(admin.ModelAdmin):
    list_display = ('cattleid', 'diseaseid', 'firstdose_status', 'seconddose_status', 'eligibility_yd', 'fdate_approved', 'sdate_approved', 'ldate_approved')
    list_filter = ('diseaseid', 'firstdose_status', 'seconddose_status', 'eligibility_yd','cattleid')
    search_fields = ('cattleid__tagno','diseaseid','disease')

class ArtificialInseminationAdmin(admin.ModelAdmin):
    list_display = ('cattleid', 'farmerid', 'date_requested', 'date_approved', 'status', 'bull', 'pregnant_status')
    list_filter = ('status', 'pregnant_status')
    search_fields = ('cattleid__tag_number', 'farmerid__first_name', 'farmerid__last_name')

admin.site.register(ArtificialInsemination, ArtificialInseminationAdmin)
admin.site.register(Disease,DiseaseAdmin)
admin.site.register(Farmer,FarmerAdmin)
admin.site.register(Vaccines,VaccinesAdmin)
admin.site.register(Cattle,CattleAdmin)
admin.site.register(Bull)
admin.site.register(Vaccination_Reg, Vaccination_RegAdmin)
admin.site.register(Vaccination_S, Vaccination_SAdmin)



