# Generated by Django 2.2.5 on 2019-10-06 05:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('observation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7105979f-0194-4049-b4a5-e21360007c29'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='observationimport',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fd0307d6-b5ee-45a1-bc30-5be8bf074c77'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='species',
            name='id',
            field=models.UUIDField(default=uuid.UUID('9bacafbc-c5f6-4fb1-8351-1e5f260caa75'), editable=False, primary_key=True, serialize=False),
        ),
    ]