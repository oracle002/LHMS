from django.urls import path
from.import views

urlpatterns=[
    path('',views.index,name='index'),
    path('ab/',views.about),
    path('reg/',views.reg),
    path('signin/',views.sign),
    path('service/',views.service),
    path('catreg/',views.cattlereg),
    path('test/',views.test),
    path('profile/',views.profile),
    path('vaccinate/',views.vaccinate),
    path('logout/', views.logout_view, name='logout'),
    path('viewv/<int:id>/', views.view_vaccine, name='view_vaccine'),
    path('booking/<int:disease_id>/', views.booking, name='booking'),
    path('bookingii/<int:disease_id>/', views.booking2, name='bookingii'),
    path('vaccination-history/', views.vaccination_history, name='vaccination_history'),
    path('chpswd/',views.changepassword),
    path('ai/',views.ai),
    path('aibooking/<int:cattle_id>/', views.book_ai, name='aibooking'),
    path('update-pregnancy-status/<int:ai_id>/', views.update_pregnancy_status, name='update_pregnancy_status'),
    path('delete-cattle/<int:cattle_id>/', views.delete_cattle, name='delete_cattle'),
    ]