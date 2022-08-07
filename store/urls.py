from django.urls import path
from . import views

urlpatterns = [
    path('customer/', views.show_customers),
    path('products/', views.show_products),
    path('order/', views.show_orders)
]
