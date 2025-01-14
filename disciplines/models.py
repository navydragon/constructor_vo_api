from django.db import models
from competenceprofile.models import Knowledge, Ability
from programs.models import Program
from products.models import Process


class Discipline(models.Model):
    name = models.TextField(null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='disciplines')
    position = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    knowledges = models.ManyToManyField(Knowledge, through='DisciplineKnowledge', related_name='disciplines')
    abilities = models.ManyToManyField(Ability, through='DisciplineAbility', related_name='disciplines')
    processes = models.ManyToManyField(Process, related_name='disciplines')


class DisciplineKnowledge(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    dk_position = models.IntegerField(null=False)


class DisciplineAbility(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    da_position = models.IntegerField(null=False)


class Semester(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='semesters')
    number = models.PositiveIntegerField(null=False)
    disciplines = models.ManyToManyField(Discipline, through='SemesterDiscipline', related_name='semesters')


class SemesterDiscipline(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    sd_position = models.IntegerField(null=False, default=0)
    zet = models.PositiveIntegerField(null=True, blank=True, default=0)
    control = models.CharField(null=True, max_length=20)
