from django.db import migrations, transaction
from posts.models import Resume
from django.contrib.auth.models import User


TEST_USERNAME1 = 'AlonShakaroff'
TEST_USERNAME2 = 'YuliSuliman'


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0006_pollfile'), ('users', '0003_add_users_test'),
    ]

    def generate_resume_test_data(apps, schema_editor):
        alon = User.objects.get(username='AlonShakaroff')
        yuli = User.objects.get(username='YuliSuliman')
        with transaction.atomic():
            resume1 = Resume(author=alon,
                             description='This is my CV, please review it :)',
                             resume_file='files/Alon Shakaroff.pdf')
            resume2 = Resume(author=yuli,
                             description="Hi everyone, I made my first CV, please review it :)",
                             resume_file='files/Yuli_CV.pdf')
            resume1.save()
            resume2.save()
    operations = [
        migrations.RunPython(generate_resume_test_data),
    ]
