# Generated by Django 2.0 on 2021-04-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='эл. почта')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='имя пользователя')),
                ('first_name', models.CharField(max_length=30, verbose_name='имя')),
                ('last_name', models.CharField(max_length=30, verbose_name='фамилия')),
                ('middle_name', models.CharField(max_length=30, verbose_name='отчество')),
                ('phone_number', models.CharField(max_length=20, verbose_name='номер телефона')),
                ('school', models.CharField(blank=True, max_length=100, null=True, verbose_name='учебное заведение')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='город')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='дата регистрации')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='последний вход')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
