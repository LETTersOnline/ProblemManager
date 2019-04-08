# Generated by Django 2.2 on 2019-04-08 17:57

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('nickname', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oj', models.CharField(max_length=255)),
                ('accepted_number', models.IntegerField(default=0)),
                ('submitted_number', models.IntegerField(default=0)),
                ('difficult_number', models.IntegerField(default=0)),
                ('origin_link', models.URLField()),
                ('content', django_mysql.models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('members', models.ManyToManyField(related_name='teams', to='problem.Member')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
