# Generated by Django 5.1.5 on 2025-03-07 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hospital", "0021_patient_is_discharged"),
    ]

    operations = [
        migrations.AddField(
            model_name="userhealth",
            name="activity_level",
            field=models.CharField(
                choices=[
                    ("sedentary", "Sedentary"),
                    ("light", "Light"),
                    ("moderate", "Moderate"),
                    ("very_active", "Very Active"),
                    ("super_active", "Super Active"),
                ],
                default="sedentary",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="userhealth",
            name="goal",
            field=models.CharField(
                choices=[
                    ("maintain", "Maintain Weight"),
                    ("lose", "Lose Weight"),
                    ("gain", "Gain Weight"),
                ],
                default="maintain",
                max_length=10,
            ),
        ),
    ]
