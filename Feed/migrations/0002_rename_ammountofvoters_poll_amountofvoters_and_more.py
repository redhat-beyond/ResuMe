# Generated by Django 4.0.3 on 2022-03-26 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Feed', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poll',
            old_name='ammountOfVoters',
            new_name='amountOfVoters',
        ),
        migrations.AlterField(
            model_name='poll',
            name='postId',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
