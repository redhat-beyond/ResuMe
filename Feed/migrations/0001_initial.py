# Generated by Django 4.0.3 on 2022-03-26 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('postId', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('datePosted', models.DateTimeField(default=django.utils.timezone.now)),
                ('ammountOfVoters', models.IntegerField(default=0)),
                ('firstFile', models.BinaryField()),
                ('secondFile', models.BinaryField(default=None)),
                ('thirdFile', models.BinaryField(default=None)),
                ('fourthFile', models.BinaryField(default=None)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('votes', models.IntegerField(default=0)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Feed.poll')),
            ],
        ),
    ]