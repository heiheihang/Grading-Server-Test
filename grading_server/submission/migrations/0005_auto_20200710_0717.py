# Generated by Django 3.0.8 on 2020-07-10 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_filesubmission_lang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filesubssmion',
            name='lang',
            field=models.CharField(choices=[('PY', 'Python 3.7')], default='PY', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filesubssmion',
            name='submission_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
