# Generated by Django 2.2 on 2020-03-29 08:11

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='state',
            field=django_fsm.FSMIntegerField(default=10),
        ),
    ]
