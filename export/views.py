from django.http import HttpResponse
from docx import Document
from docx.shared import Pt

from io import BytesIO
from urllib.parse import quote
from programs.models import Program
from django.shortcuts import get_object_or_404
from django.db.models import Count


def export_design(request, program_id):
    # Создаем docx файл
    doc = Document()

    # программа
    program = get_object_or_404(Program, id=program_id)
    doc.add_heading(f'Дизайн программы «{program.direction_id.code} {program.direction_id.name} {program.profile}»', 0)
    doc.add_heading('Реконструкция деятельности',1)
    doc.add_heading('Продукты', 2)

    for index,product in enumerate( program.products.all()):
        pr_number = index + 1
        doc.add_paragraph(f'{pr_number}. {product.name}', style='List Bullet')
    doc.add_heading('Процессы', 2)
    for pr_index, product in enumerate(program.products.all()):
        product_number = pr_index + 1
        doc.add_heading(f'Продукт «{product_number}. {product.name}»', 3)
        for st_index, stage in enumerate(product.stages.all()):
            stage_number = st_index + 1
            doc.add_paragraph(f'Этап {product_number}.{stage_number}. {stage.name}', style='List Bullet')
            for proc_index, process in enumerate(stage.processes.all()):
                process_number = proc_index + 1
                doc.add_paragraph(f'{product_number}.{stage_number}.{process_number} {process.name}', style='List Bullet 2')

    doc.add_heading('Компетентностный профиль', 1)

    doc.add_heading('Перечень знаний и умений', 2)
    for index, ability in enumerate(program.abilities.all()):
        ability_number = index + 1
        doc.add_paragraph(f'{ability_number}. {ability.name}', style='List Bullet')
        for kn_index, knowledge in enumerate(ability.knowledges.all()):
            knowledge_number = kn_index + 1
            doc.add_paragraph(f'{ability_number}.{knowledge_number} {knowledge.name}', style='List Bullet 2')

    doc.add_heading('Сопоставление процессов со знаниями и умениями', 2)

    for product in program.products.order_by('position'):
        for stage in product.stages.order_by('position'):
            for process in stage.processes.order_by('position'):
                doc.add_paragraph(f'Процесс: {process.name}', style='List Bullet')
                for ability in process.abilities.order_by('postion'):
                    doc.add_paragraph(f'Умение: {ability.name}', style='List Bullet 2')
                    for knowledge in ability.knowledges.order_by('position'):
                        doc.add_paragraph(f'Знание: {knowledge.name}', style='List Bullet 3')

    # process_count_for_program = Program.objects.filter(id=program_id).aggregate(process_count=Count('products__stages__processes'))


    # table = doc.add_table(rows=process_count_for_program['process_count'], cols=3)
    # table.style='Table Grid'

    doc.add_heading('Дисциплины', 1)
    for index, semester in enumerate(program.semesters.order_by('number'), start=1):
        doc.add_paragraph(f'Семестр №{semester.number}', style='List Bullet')

        for disc_index, discipline in enumerate(semester.disciplines.all(), start=1):
            doc.add_paragraph(f'{discipline.name}', style='List Bullet 2')



    # Сохраняем документ в BytesIO
    output = BytesIO()
    doc.save(output)
    output.seek(0)

    filename = quote('Дизайн программы.docx')
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    response.write(output.read())

    return response


def add_multilevel_list(paragraph, text, level):
    run = paragraph.add_run(text)
    # Устанавливаем уровень списка
    paragraph_style = 'List Bullet'
    #paragraph.style = 'List Number ' + str(level)


