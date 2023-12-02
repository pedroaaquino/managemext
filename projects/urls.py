from django.urls import path, include
from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.list_projects, name='index'),
    path('create/', views.create_project, name='create'),
    path('<int:project_id>/', views.detail_project, name='detail'),
    path('update/<int:project_id>/', views.update_project, name='update'),
    path('delete/<int:project_id>/', views.delete_project, name='delete'),
    path('<int:project_id>/tarefa/', views.create_tarefa, name='tarefa'),
    path('<int:project_id>/tarefa/<int:tarefa_id>/', views.update_tarefa, name='update_tarefa'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('nucleos/', views.NucleoListView.as_view(), name='nucleos'),
    path('nucleos/create', views.NucleoCreateView.as_view(), name='create-nucleo'),
    path('nucleos/<int:nucleo_id>', views.detail_nucleo, name='detail_nucleo'),
]
