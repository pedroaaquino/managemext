from django.contrib import admin

from .models import Project, Tarefa, Nucleo

admin.site.register(Project)
admin.site.register(Tarefa)
admin.site.register(Nucleo)