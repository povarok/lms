# Generated by Django 2.0 on 2020-06-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testgroupconstructor',
            name='tests',
            field=models.ManyToManyField(related_name='groups', to='polls.TrainingApparatus', verbose_name='тесты'),
        ),
    ]