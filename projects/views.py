from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from .temp_data import project_data
from django.shortcuts import render, get_object_or_404
from .models import Project
from django.views import generic
from .models import Project, Tarefa
from .forms import ProjectForm, TarefaForm


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


def create_tarefa(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa_name = form.cleaned_data['name']
            tarefa_descricao = form.cleaned_data['descricao']
            tarefa_data_entrega = form.cleaned_data['data_entrega']
            tarefa_concluida = form.cleaned_data.get('concluida', False)
            tarefa = Tarefa(name=tarefa_name,
                          descricao=tarefa_descricao,
                          data_entrega=tarefa_data_entrega,
                          concluida=tarefa_concluida,
                          projeto = project
                          )
            tarefa.save()
            return HttpResponseRedirect(
                reverse('projects:detail', args=(project_id, )))
    else:    
        form = ProjectForm()
    context = {'form': form, 'project': project}
    return render(request, 'projects/tarefa.html', context)


def update_tarefa(request, project_id, tarefa_id):
    project = get_object_or_404(Project, pk=project_id)
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)

    if request.method == "POST":
        form = TarefaForm(request.POST)
        if form.is_valid():
            tarefa.name = form.cleaned_data['name']
            tarefa.descricao = form.cleaned_data['descricao']
            tarefa.data_entrega = form.cleaned_data['data_entrega']
            tarefa.concluida = form.cleaned_data.get('concluida', False)
            tarefa.save()
            return HttpResponseRedirect(
                reverse('projects:detail', args=(project.id, )))
    else:
        form = TarefaForm(
            initial={
                'name': tarefa.name,
                'data_entrega': tarefa.data_entrega
            })
        
    context = {'tarefa': tarefa, 'project': project, 'form': form}
    return render(request, 'projects/update_tarefa.html', context)
