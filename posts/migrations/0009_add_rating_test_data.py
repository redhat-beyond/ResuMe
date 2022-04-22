from django.db import migrations, transaction
from posts.models import Rating, Resume
from django.contrib.auth.models import User
import random


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0008_add_comment_test_data'),
    ]

    def generate_rating_test_data(apps, schema_editor):
        resume1 = Resume.objects.get(author__username='AlonShakaroff')
        resume2 = Resume.objects.get(author__username='YuliSuliman')
        rating_users = User.objects.exclude(username='AlonShakaroff').exclude(username='YuliSuliman')
        with transaction.atomic():
            for i in range(0, rating_users.__len__()):
                resume = resume1
                if(i % 2 == 0):
                    resume = resume2

                rating = Rating(author=rating_users[i], resume=resume, design_rating=random.randrange(1, 5),
                                grammar_rating=random.randrange(1, 5), conciseness_rating=random.randrange(1, 5),
                                skill_relevance_rating=random.randrange(1, 5))
                rating.save()

    operations = [
        migrations.RunPython(generate_rating_test_data),
    ]
