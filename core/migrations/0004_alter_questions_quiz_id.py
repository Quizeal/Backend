# Generated by Django 3.2.4 on 2021-07-18 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_questions_question_marks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='quiz_id',
            field=models.IntegerField(),
        ),
    ]
