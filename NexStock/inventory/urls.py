from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('pages-contact/', views.contact, name='contact'),
    path('forms-layouts/', views.forms_layouts, name='forms_layouts'),
    path('tables-data/', views.tables_data, name='tables_data'),
    path('charts-chartjs/', views.charts_chartjs, name='charts_chartjs'),
    path('users-profile/', views.users_profile, name='users_profile'),
    path('pages-register/', views.pages_register, name='pages_register'),
    path('pages-login/', views.pages_login, name='pages_login')
]