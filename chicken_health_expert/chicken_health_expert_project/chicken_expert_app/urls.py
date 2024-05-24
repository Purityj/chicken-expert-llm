from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('expert_llm', views.expert_llm, name='expert_llm'),
    path('disease_frequency/', views.show_disease_frequency, name='disease_frequency'),
    path('find_vets/', views.find_vets, name='find_vets'),
]