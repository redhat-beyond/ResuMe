from django.db import migrations, transaction


class Migration(migrations.Migration):
    
    dependencies = [
        ('users', '0001_initial'),
    ]

    def generate_user_test_data(apps, schema_editor):
        from django.contrib.auth.models import User

        users_test_data = [
            ("AlonShakaroff","Alon", "Shakaroff", "test$1234" ,"alon@gmail.com", "test/alon.jpg"),
            ("OmerCohenShor","Omer", "Cohen-Shor", "test$5678" , "omer@gmail.com", "test/omer.jpg"),
            ("TomerNewman","Tomer", "Newman", "test$8910" , "tomer@gmail.com", "test/tomer.jpg"),
            ("YuliSuliman","Yuli", "Suliman", "test$3643" , "yuli@gmail.com", "test/yuli.jpg"),
            ("MatanPeretz","Matan", "Peretz", "test$8979" , "matan@gmail.com", "test/matan.jpg")
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
