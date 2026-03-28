from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_profession_user_residence_alter_user_last_login"),
    ]

    operations = [
        migrations.DeleteModel(
            name="OTPCode",
        ),
    ]
