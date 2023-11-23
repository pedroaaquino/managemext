from django.forms import ModelForm
from .models import Project


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