from django.core.management.base import BaseCommand
from assessment.models import QuestionType


class Command(BaseCommand):
    help = 'Загружаем список типов вопросов'

    def handle(self, *args, **options):
        QuestionType.objects.bulk_create([
            QuestionType(name='Выбор одного правильного ответа', type='one-answer'),
            QuestionType(name='Выбор нескольких правильных ответов', type='multi-answer'),
            QuestionType(name='Вопрос с открытым ответом', type='open-answer'),
            QuestionType(name='Установление последовательности', type='sequence-answer'),
            QuestionType(name='Установление соответствия', type='conformity-answer'),
        ])
        self.stdout.write(self.style.SUCCESS('Successfully loaded QuestionTypes'))
