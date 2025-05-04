from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('subcategory/<slug:slug>/', views.subcategory_detail, name='subcategory_detail'),
]
