# Generated by Django 3.0.8 on 2020-07-14 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0004_auto_20200712_1948'),
        ('submission', '0005_auto_20200710_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='filesubssmion',
            name='problem',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='problem.ProblemModel'),
        ),
    ]
