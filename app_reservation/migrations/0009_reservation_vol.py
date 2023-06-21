# Generated by Django 4.2.1 on 2023-05-24 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app_reservation", "0008_voiture"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reservation_Vol",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField()),
                (
                    "utilisateur",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="utilisateur",
                        to="app_reservation.utilisateur",
                    ),
                ),
                (
                    "vol",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vol",
                        to="app_reservation.vol",
                    ),
                ),
            ],
        ),
    ]
