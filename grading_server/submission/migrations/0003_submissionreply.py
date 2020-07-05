# Generated by Django 3.0.8 on 2020-07-05 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_filesubssmion_graded'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField(default=False)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submission.FileSubssmion')),
            ],
        ),
    ]
