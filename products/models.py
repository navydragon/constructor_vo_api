from django.db import models
from programs.models import Program


class Product(models.Model):
    name = models.CharField(max_length=500)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='products')
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name

class LifeStage(models.Model):
    name = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'life_stages'

    def __str__(self):
        return self.name


class Process(models.Model):
    name = name = models.TextField()
    stage = models.ForeignKey(LifeStage, on_delete=models.CASCADE)
    position = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'processes'

    def __str__(self):
        return self.name
