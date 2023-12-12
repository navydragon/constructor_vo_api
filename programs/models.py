from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Direction(models.Model):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=500)
    level = models.CharField(max_length=500)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'education_directions'  # This is optional if you want to specify the exact table name

    def __str__(self):
        return self.name


class EducationLevel(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        db_table = 'education_levels'  # This is optional if you want to specify the table name

    def __str__(self):
        return self.name

class ProgramRole(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'program_roles'


class Program(models.Model):
    FORMS = [
        ('Очная', 'Очная'),
        ('Очно-заочная', 'Очно-заочная'),
        ('Заочная', 'Заочная'),
    ]
    profile = models.CharField(max_length=255)
    annotation = models.TextField(null=True, blank=True)
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='programs')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    level_id = models.ForeignKey('EducationLevel', on_delete=models.RESTRICT, default=1)
    direction_id = models.ForeignKey('Direction', on_delete=models.CASCADE, default=1)
    form = models.CharField(
        max_length=20,
        choices=FORMS,
        default='Очная'
    )
    max_semesters = models.PositiveIntegerField(null=True)
    class Meta:
        db_table = 'programs'

    def __str__(self):
        return self.profile


class ProgramUser(models.Model):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='work_programs', null=True,
        blank=True
    )
    program_id = models.ForeignKey(
        'Program', on_delete=models.CASCADE, related_name='participants',
        null=True, blank=True
    )
    role_id = models.ForeignKey(
        'ProgramRole', on_delete=models.CASCADE,
        null=True, blank=True
    )
    class Meta:
        db_table = 'program_users'