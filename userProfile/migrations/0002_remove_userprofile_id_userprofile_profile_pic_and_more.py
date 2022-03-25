# Generated by Django 4.0.3 on 2022-03-25 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userProfile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='id',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='profile-icon.png', upload_to='profiles/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, unique=True),
        ),
    ]