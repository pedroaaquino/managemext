from django.forms import ModelForm
from .models import Project, Tarefa


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'data_entrega',
        ]
        labels = {
            'name': 'Nome',
            'release_year': 'Data de Entrega',
        }

class TarefaForm(ModelForm):
    class Meta:
        model = Tarefa
        fields = [
            'name',
            'descricao',
            'data_entrega',
            'concluida',
        ]
        labels = {
            'name': 'Nome',
            'descricao': 'Descrição',
            'data_entrega': 'Data de Entrega',
            'concluida': 'Tarefa Concluída?',
        }
