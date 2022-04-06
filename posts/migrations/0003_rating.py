# Generated by Django 4.0.3 on 2022-03-31 12:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('rating_id',
                 models.AutoField(primary_key=True,
                                  serialize=False)),
                ('design_rating',
                 models.IntegerField(validators=[django.core.validators.MaxValueValidator(5),
                                                 django.core.validators.MinValueValidator(1)])),
                ('skill_relevance_rating',
                 models.IntegerField(validators=[django.core.validators.MaxValueValidator(5),
                                                 django.core.validators.MinValueValidator(1)])),
                ('grammar_rating',
                 models.IntegerField(validators=[django.core.validators.MaxValueValidator(5),
                                                 django.core.validators.MinValueValidator(1)])),
                ('conciseness_rating',
                 models.IntegerField(validators=[django.core.validators.MaxValueValidator(5),
                                                 django.core.validators.MinValueValidator(1)])),
                ('author',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to=settings.AUTH_USER_MODEL)),
                ('resume',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='posts.resume')),
            ],
        ),
    ]