# Generated by Django 3.1 on 2020-08-19 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0009_filesubmission_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesubmission',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='filesubmission',
            name='feedback',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]