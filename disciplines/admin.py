from django.contrib import admin
from .models import Discipline, DisciplineKnowledge, DisciplineAbility, Semester, SemesterDiscipline


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'position', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('program',)
    ordering = ('position',)


@admin.register(DisciplineKnowledge)
class DisciplineKnowledgeAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'knowledge', 'dk_position')
    list_filter = ('discipline',)
    ordering = ('dk_position',)


@admin.register(DisciplineAbility)
class DisciplineAbilityAdmin(admin.ModelAdmin):
    list_display = ('discipline', 'ability', 'da_position')
    list_filter = ('discipline',)
    ordering = ('da_position',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('program', 'number')
    list_filter = ('program',)
    ordering = ('number',)


@admin.register(SemesterDiscipline)
class SemesterDisciplineAdmin(admin.ModelAdmin):
    list_display = ('semester', 'discipline', 'sd_position', 'zet', 'control')
    list_filter = ('semester', 'discipline')
    ordering = ('sd_position',)
