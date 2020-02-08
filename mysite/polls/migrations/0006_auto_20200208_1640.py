# Generated by Django 2.0 on 2020-02-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20200202_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercise',
            name='correct_answers',
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_index',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trainingapparatus',
            name='description',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='trainingtest',
            name='time_start',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercisetypes',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]