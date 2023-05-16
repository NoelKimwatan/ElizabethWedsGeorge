# Generated by Django 4.2.1 on 2023-05-16 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gifts", "0007_remove_gift_email_remove_gift_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gift",
            name="status",
            field=models.IntegerField(
                choices=[(1, "Created"), (2, "Failed"), (3, "Completed")], default=1
            ),
        ),
    ]