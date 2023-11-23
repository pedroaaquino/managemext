from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .temp_data import project_data
from django.shortcuts import render, get_object_or_404
from .models import Project
from django.views import generic
from .models import Project
from .forms import ProjectForm

def detail_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    return render(request, 'projects/detail.html', context)

def list_projects(request):
    project_list = Project.objects.all()
    context = {"project_list": project_list}
    return render(request, 'projects/index.html', context)

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_name = form.cleaned_data['name']
            project_data_entrega = form.cleaned_data['data_entrega']
            project = Project(name=project_name,
                          data_entrega=project_data_entrega)
            project.save()
            return HttpResponseRedirect(
                reverse('projects:detail', args=(project.id, )))
    else:
        form = ProjectForm()
    context = {'form': form}
    return render(request, 'projects/create.html', context)

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project.name = form.cleaned_data['name']
            project.data_entrega = form.cleaned_data['data_entrega']
            project.save()
            return HttpResponseRedirect(
                reverse('projects:detail', args=(project.id, )))
    else:
        form = ProjectForm(
            initial={
                'name': project.name,
                'data_entrega': project.data_entrega
            })

    context = {'project': project, 'form': form}
    return render(request, 'projects/update.html', context)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        return HttpResponseRedirect(reverse('projects:index'))

    context = {'project': project}
    return render(request, 'projects/delete.html', context)