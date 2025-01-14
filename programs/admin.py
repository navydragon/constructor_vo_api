from django.contrib import admin
from .models import (
    Direction, EducationLevel, ProgramRole, Program, ProgramUser,
    NsiType, Ministry, Nsi
)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'level', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('level',)
    ordering = ('code',)


@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(ProgramRole)
class ProgramRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id','profile', 'author', 'direction_id', 'level_id', 'form', 'created_at', 'updated_at')
    search_fields = ('profile',)
    list_filter = ('form', 'direction_id', 'level_id')
    ordering = ('profile',)


@admin.register(ProgramUser)
class ProgramUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'program_id', 'role_id')
    list_filter = ('program_id', 'role_id')
    ordering = ('program_id',)


@admin.register(NsiType)
class NsiTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'part', 'active', 'code')
    search_fields = ('name', 'code')
    list_filter = ('active',)
    ordering = ('position',)


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'short_nominative', 'short_genitive', 'created_at', 'updated_at')
    search_fields = ('fullname', 'short_nominative', 'short_genitive')
    ordering = ('fullname',)


@admin.register(Nsi)
class NsiAdmin(admin.ModelAdmin):
    list_display = (
        'type', 'program', 'author', 'nsiName', 'nsiCode', 'nsiCity',
        'nsiYear', 'nsiFullName', 'nsiMinistry', 'created_at', 'updated_at'
    )
    search_fields = ('nsiName', 'nsiCode', 'nsiFullName')
    list_filter = ('type', 'program', 'nsiMinistry')
    ordering = ('nsiName',)
