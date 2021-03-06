# Generated by Django 3.1 on 2020-08-19 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('elo', models.IntegerField()),
                ('profile_picture', models.ImageField(upload_to='users_profile_pic')),
            ],
        ),
    ]
