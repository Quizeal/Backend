# Generated by Django 3.2.5 on 2021-08-26 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.TextField()),
                ('question_type', models.IntegerField(choices=[(1, 'single_ans'), (2, 'multiple_ans')], default=1)),
                ('question_marks', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_token', models.CharField(max_length=6, unique=True)),
                ('quiz_name', models.TextField()),
                ('username', models.CharField(max_length=150)),
                ('start_time', models.TimeField()),
                ('duration', models.DurationField()),
                ('date', models.DateField()),
                ('total_marks', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuizOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.TextField()),
                ('is_correct', models.BooleanField()),
                ('is_active', models.BooleanField(default=True)),
                ('question_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='core.questions')),
            ],
        ),
        migrations.CreateModel(
            name='QuizMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('marks', models.IntegerField()),
                ('total_marks', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='core.quizdetails')),
            ],
        ),
        migrations.CreateModel(
            name='QuizAnswered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('option_name', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='core.questions')),
                ('quiz_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.quizdetails')),
            ],
        ),
        migrations.AddField(
            model_name='questions',
            name='quiz_details',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='core.quizdetails'),
        ),
    ]
