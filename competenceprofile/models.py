from django.db import models
from products.models import Process
from programs.models import Program


class Ability(models.Model):
    name = models.TextField( null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='abilities')
    position = models.IntegerField(null=False)
    processes = models.ManyToManyField(Process, related_name='abilities')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'abilities'  # Явно указываем название таблицы в базе данных

    def __str__(self):
        return self.name
