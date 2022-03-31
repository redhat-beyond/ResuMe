from django.db import migrations, transaction
from posts.models import Rating, Resume
import random


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_rating'),
    ]

    def generate_post_test_data(apps, schema_editor):
        from django.contrib.auth.models import User
        users = User.objects.all()

        with transaction.atomic():
            resume = Resume(author=users[0], description="Hi this is my resume file :) " +
                            users[0].first_name, resume_file="files/Alon_Shakaroffs_resume.pdf")
            resume.save()
            r = range(2, 5)
            for i in r:
                rating = Rating(author=users[i], resume=resume, design_rating=random.randrange(1, 5),
                                grammar_rating=random.randrange(1, 5), conciseness_rating=random.randrange(1, 5),
                                skill_relevance_rating=random.randrange(1, 5))
                rating.save()

    operations = [
        migrations.RunPython(generate_post_test_data),
    ]
