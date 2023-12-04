from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .temp_data import project_data
from django.shortcuts import render, get_object_or_404, reverse
from .models import Project
from django.views import generic
from .models import Project, Tarefa, Nucleo
from .forms import ProjectForm, TarefaForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from accounts.views import user_list
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



def detail_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    context = {'project': project}
    return render(request, 'projects/detail.html', context)

def list_projects(request):
    project_list = Project.objects.all()
    context = {"project_list": project_list}
    return render(request, 'projects/index.html', context)

@login_required
@permission_required('projects.add_project')
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

# Escopo necessário para acessar o Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']


@login_required
@permission_required('projects.add_project')
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
            # Autenticação com o Google Calendar
            flow = InstalledAppFlow.from_client_secrets_file(
                'managemext.json', scopes=SCOPES
            )
            creds = flow.run_local_server(host='0.0.0.0', port=0)

            # Criação do evento no Google Calendar
            service = build('calendar', 'v3', credentials=creds)
            event = {
                'summary': tarefa_name,
                'description': tarefa_descricao,
                'start': {'dateTime': tarefa_data_entrega.isoformat()},
                'end': {'dateTime': tarefa_data_entrega.isoformat()},
            }
            service.events().insert(calendarId='primary', body=event).execute()
            return HttpResponseRedirect(
                reverse('projects:detail', args=(project_id, )))
    else:    
        form = ProjectForm()
    context = {'form': form, 'project': project}
    return render(request, 'projects/tarefa.html', context)


@login_required
@permission_required('projects.add_project')
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

class NucleoListView(generic.ListView):
    model = Nucleo
    template_name = 'projects/nucleos.html'


class NucleoCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Nucleo
    template_name = 'projects/create_nucleo.html'
    fields = ['name', 'projects']
    success_url = reverse_lazy('projects:nucleos')
    permission_required = 'projects.add_nucleo'

def detail_nucleo(request, nucleo_id):  
    nucleo = get_object_or_404(Nucleo, pk=nucleo_id)
    projects_list = Project.objects.filter(nucleo=nucleo_id)
    context = {'nucleo': nucleo,  'post_list': projects_list}
    return render(request, 'projects/detail_nucleo.html', context)


@login_required
@permission_required('auth.change_user')
def change_user_group(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_id = request.POST.get('group_id')

        user = get_object_or_404(User, id=user_id)
        group = get_object_or_404(Group, id=group_id)

        user.groups.clear() 
        user.groups.add(group)  
    users = User.objects.all()
    groups = Group.objects.all()
    return render(request, 'projects/list_users.html', {'users': users, 'groups': groups})
