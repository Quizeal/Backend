# Generated by Django 3.2.4 on 2021-07-24 21:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210725_0220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizoptions',
            name='question_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.questions'),
        ),
    ]