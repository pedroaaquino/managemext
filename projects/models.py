from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=255)
    data_entrega = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.data_entrega})'
    

class Tarefa(models.Model):
    name = models.CharField(max_length=255, default='tarefa')
    descricao = models.CharField(max_length=255)
    data_entrega = models.DateField()
    projeto = models.ForeignKey(Project, on_delete=models.CASCADE)
    concluida = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.name} - {self.descricao}'

