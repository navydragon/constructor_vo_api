from django.db import models
import uuid

from django.contrib.auth import get_user_model
from competenceprofile.models import Knowledge, Ability

User = get_user_model()


class QuestionType(models.Model):
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    type = models.CharField(max_length=191, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question_type = models.ForeignKey('QuestionType', on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    text2 = models.TextField(null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    position = models.IntegerField(default=0)
    image = models.FileField(null=True)

    def __str__(self):
        return f"{self.text} - {'(+)' if self.is_correct else '(-)'}"


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name
