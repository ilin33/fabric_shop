from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('success/', views.order_success, name='order_success'),

    # API для Нової Пошти
    path('api/nova-poshta/cities/', views.nova_poshta_cities, name='nova_poshta_cities'),
    path('api/nova-poshta/warehouses/', views.nova_poshta_warehouses, name='nova_poshta_warehouses'),

    # API для Укрпошти
    path('api/ukrposhta/cities/', views.ukrposhta_cities, name='ukrposhta_cities'),
    path('api/ukrposhta/warehouses/', views.ukrposhta_warehouses, name='ukrposhta_warehouses'),
]