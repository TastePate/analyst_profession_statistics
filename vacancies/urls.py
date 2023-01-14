from django.urls import path

from vacancies import views

urlpatterns = [
    path('', views.main),
    path('main/', views.main),
    path('demand/', views.demand),
    path('geography/', views.geography),
    path('skills/', views.skills),
    path('last_vacancies/', views.last_vacancies),
]