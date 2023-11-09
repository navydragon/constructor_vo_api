from django.db import models
from competenceprofile.models import Knowledge
from programs.models import Program


class Discipline(models.Model):
    name = models.TextField(null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='disciplines')
    position = models.IntegerField(null=False)
    knowledges = models.ManyToManyField(Knowledge, related_name='disciplines')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
