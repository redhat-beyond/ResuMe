from django.db import migrations, transaction
from posts.models import Resume, Comment
from django.contrib.auth.models import User


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0007_add_resume_test_data'),
    ]

    def generate_comment_test_data(apps, schema_editor):
        tomer = User.objects.get(username='TomerNewman')
        omer = User.objects.get(username='OmerCohenShor')
        resume1 = Resume.objects.get(author__username='AlonShakaroff')
        resume2 = Resume.objects.get(author__username='YuliSuliman')

        with transaction.atomic():
            comment1 = Comment(post=resume1,
                               author=tomer,
                               comment_text="Really nice resume")
            comment1.save()
            comment2 = Comment(post=resume2,
                               author=omer,
                               comment_text=("Overall good resume, but I think"
                                             "you should learn more programming languages"))
            comment2.save()

    operations = [
        migrations.RunPython(generate_comment_test_data),
    ]
