from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_profile_profession'),
    ]

    def generate_user_test_data(apps, schema_editor):
        from django.contrib.auth.models import User

        # Create a super user
        superuser = User()
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.username = 'admin'
        superuser.email = 'admin@gmail.com'
        superuser.set_password('admin1234')
        superuser.save()
        superuser.profile.profession = "ResuMe Super User"
        superuser.profile.bio = "Hi I am the Resume manager :)"
        superuser.profile.profile_pic = "profile_pics/admin.jpg"
        superuser.profile.save()
        # Create normal users
        users_test_data = [
            ("AlonShakaroff", "Alon", "Shakaroff", "alon1234",
             "alon@gmail.com", "profile_pics/alon.jpg", "Software Developer"),
            ("OmerCohenShor", "Omer", "Cohen-Shor", "omer1234", "omer@gmail.com",
             "profile_pics/omer.jpg", "Frontend Developer"),
            ("TomerNewman", "Tomer", "Newman", "tomer1234",
             "tomer@gmail.com", "profile_pics/tomer.jpeg", "Software Developer"),
            ("YuliSuliman", "Yuli", "Suliman", "yuli1234",
             "yuli@gmail.com", "profile_pics/yuli.jpg", "Software Developer"),
            ("MatanPeretz", "Matan", "Peretz", "matan1234",
             "matan@gmail.com", "profile_pics/matan.jpg", "Backend Developer")
        ]

        with transaction.atomic():
            for USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL, PROFILE_PIC, PROFFESION in users_test_data:
                user = User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, email=EMAIL)
                user.set_password(PASSWORD)
                user.save()
                user.profile.bio = "Hi my name is " + FIRSTNAME + " " + LASTNAME
                user.profile.profile_pic = PROFILE_PIC
                user.profile.profession = PROFFESION
                user.profile.save()
    operations = [
        migrations.RunPython(generate_user_test_data),
    ]
