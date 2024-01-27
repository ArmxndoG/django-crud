from django.contrib import admin
from .models import Task
# Register your models here.

#Clase para añadir un campo de solo lectura (fecha de creación)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )

#Añadiendo el registro para la tabla 'Tarea', en el panel de administrador
admin.site.register(Task,TaskAdmin)



