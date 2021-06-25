# Generated by Django 3.2.4 on 2021-06-24 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0002_quiz_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz_data',
            name='correct_answer',
        ),
        migrations.RemoveField(
            model_name='quiz_data',
            name='question',
        ),
        migrations.RemoveField(
            model_name='quiz_data',
            name='selected_answer',
        ),
        migrations.CreateModel(
            name='quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('correct_answer', models.CharField(max_length=200)),
                ('selected_answer', models.CharField(max_length=200)),
                ('status', models.IntegerField()),
                ('quiz_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quizapp.quiz_data')),
            ],
        ),
    ]