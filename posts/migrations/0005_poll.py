# Generated by Django 4.0.3 on 2022-04-05 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('post_ptr', models.OneToOneField(
                    auto_created=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    parent_link=True,
                    primary_key=True,
                    serialize=False,
                    to='posts.post')),
            ],
            bases=('posts.post',),
        ),
    ]