# Generated by Django 3.2.4 on 2021-08-01 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_quizdetails_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizmarks',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]