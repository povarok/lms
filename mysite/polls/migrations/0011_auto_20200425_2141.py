# Generated by Django 2.0 on 2020-04-25 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0010_auto_20200406_0631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='test',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='polls.TrainingTest', verbose_name='Тест'),
        ),
    ]
