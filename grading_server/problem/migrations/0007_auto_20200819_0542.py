# Generated by Django 3.1 on 2020-08-19 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0006_delete_problemtestmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problemtestpairmodel',
            old_name='test_suite',
            new_name='suite',
        ),
        migrations.RenameField(
            model_name='problemtestsuitemodel',
            old_name='test_suite_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='problemtestsuitemodel',
            old_name='problem_suite_number',
            new_name='suite_number',
        ),
    ]