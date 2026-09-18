from django.urls import path
from django.contrib.auth import views as auth
from . import views
urlpatterns = [
 path('', views.home, name='home'), path('register/', views.register, name='register'), path('signup/', views.register, name='signup'),
 path('login/', views.GardenLoginView.as_view(), name='login'), path('logout/', views.user_logout, name='logout'),
 path('dashboard/', views.dashboard, name='dashboard'), path('gardens/', views.gardens, name='gardens'), path('gardens/add/', views.garden_add, name='garden_add'),
 path('plants/', views.plants, name='plants'), path('my-plants/add/', views.plant_add, name='plant_add'), path('recommendations/', views.recommendations, name='recommendations'),
 path('disease-detection/', views.disease_detection, name='disease_detection'), path('watering/', views.watering, name='watering'), path('fertilizer/', views.fertilizer, name='fertilizer'),
 path('tasks/', views.tasks, name='tasks'), path('tasks/add/', views.task_add, name='task_add'), path('tasks/<int:pk>/complete/', views.complete_task, name='complete_task'),
 path('assistant/', views.assistant, name='assistant'), path('reports/', views.reports, name='reports'), path('weather/', views.weather, name='weather'),
 path('garden-manager/', views.garden_manager, name='garden_manager'), path('garden-manager/<str:kind>/', views.manager_collection, name='manager_collection'),
]
