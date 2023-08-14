from django.urls import path
from . import views



urlpatterns = [
    path('create/', views.vehicle_create, name='vehicle_create'),
    path('<int:pk>/update/', views.vehicle_update, name='vehicle_update'),
    path('<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    path('register/', views.register_user, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
]