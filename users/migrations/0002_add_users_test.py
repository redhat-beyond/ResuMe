from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
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
        # Create normal users
        users_test_data = [
            ("AlonShakaroff", "Alon", "Shakaroff", "test$1234", "alon@gmail.com", "profile_pics/alon.jpg"),
            ("OmerCohenShor", "Omer", "Cohen-Shor", "test$5678", "omer@gmail.com", "profile_pics/omer.jpg"),
            ("TomerNewman", "Tomer", "Newman", "test$8910", "tomer@gmail.com", "profile_pics/tomer.jpeg"),
            ("YuliSuliman", "Yuli", "Suliman", "test$3643", "yuli@gmail.com", "profile_pics/yuli.jpg"),
            ("MatanPeretz", "Matan", "Peretz", "test$8979", "matan@gmail.com", "profile_pics/matan.jpg")
        ]

        with transaction.atomic():
            for USERNAME, FIRSTNAME, LASTNAME, PASSWORD, EMAIL, PROFILE_PIC in users_test_data:
                user = User(username=USERNAME, first_name=FIRSTNAME, last_name=LASTNAME, password=PASSWORD, email=EMAIL)
                user.save()
                user.profile.bio = "Hi my name is " + FIRSTNAME + " " + LASTNAME
                user.profile.profile_pic = PROFILE_PIC
                user.profile.save()
    operations = [
        migrations.RunPython(generate_user_test_data),
    ]
