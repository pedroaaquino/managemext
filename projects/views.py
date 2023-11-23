from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .temp_data import project_data
from django.shortcuts import render

def detail_project(request, project_id):
    project = project_data[project_id - 1]
    return HttpResponse(
        f'Detalhes do projeto {project["name"]} ({project["data_entrega"]})')

def list_projects(request):
    context = {"project_list": project_data}
    return render(request, 'projects/index.html', context)

def detail_project(request, project_id):
    context = {'project': project_data[project_id - 1]}
    return render(request, 'projects/detail.html', context)

def create_project(request):
    if request.method == 'POST':
        project_data.append({
            'name': request.POST['name'],
            'data_entrega': request.POST['data_entrega'],
        })
        return HttpResponseRedirect(
            reverse('projects:detail', args=(len(project_data), )))
    else:
        return render(request, 'projects/create.html', {})