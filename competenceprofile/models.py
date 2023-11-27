from django.db import models
from products.models import Process
from programs.models import Program


class Ability(models.Model):
    name = models.TextField(null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE,
                                related_name='abilities')
    position = models.IntegerField(null=False)
    processes = models.ManyToManyField(Process,  through='ProcessAbility',related_name='abilities')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'abilities'

    def __str__(self):
        return self.name

    def update_ak_positions(self, start_position):
        abilities_to_update = self.knowledges.through.objects.filter(
            ability_id=self.id,
            ak_position__gt=start_position
        )

        for ability_knowledge in abilities_to_update:
            ability_knowledge.ak_position -= 1
            ability_knowledge.save()

class ProcessAbility(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    ability = models.ForeignKey(Ability,  on_delete=models.CASCADE)
    pa_position = models.IntegerField(null=False)

class Knowledge(models.Model):
    name = models.TextField(null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='knowledges')
    position = models.IntegerField(null=False)
    abilities = models.ManyToManyField(Ability, through='AbilityKnowledge', related_name='knowledges')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'knowledges'

    def __str__(self):
        return self.name

class AbilityKnowledge(models.Model):
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    ak_position = models.IntegerField(null=False)