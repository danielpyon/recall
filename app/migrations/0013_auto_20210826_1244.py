# Generated by Django 3.2.5 on 2021-08-26 19:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_snippet_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='id',
        ),
        migrations.AlterField(
            model_name='snippet',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
