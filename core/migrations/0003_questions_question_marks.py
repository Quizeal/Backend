# Generated by Django 3.2.4 on 2021-07-18 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_quizdetails_quiz_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='question_marks',
            field=models.IntegerField(null=True),
        ),
    ]