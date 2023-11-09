from django.db import models
from products.models import Process
from programs.models import Program


class Ability(models.Model):
    name = models.TextField(null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE,
                                related_name='abilities')
    position = models.IntegerField(null=False)
    processes = models.ManyToManyField(Process, related_name='abilities')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'abilities'

    def __str__(self):
        return self.name


class Knowledge(models.Model):
    name = models.TextField(null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='knowledges')
    position = models.IntegerField(null=False)
    abilities = models.ManyToManyField(Ability, related_name='knowledges')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'knowledges'

    def __str__(self):
        return self.name
