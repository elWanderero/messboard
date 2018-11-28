# Generated by Django 2.1.3 on 2018-11-28 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [
        ("base", "0001_initial"),
        ("base", "0002_user_foo"),
        ("base", "0003_auto_20181121_1147"),
    ]

    initial = True

    dependencies = []  # type: ignore

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("text", models.TextField()),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
            options={"db_table": "message", "managed": True},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=32, unique=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("deactivated", models.DateTimeField(blank=True, null=True)),
                ("active", models.BooleanField()),
                (
                    "public_key",
                    models.CharField(blank=True, max_length=178, null=True),
                ),
                ("email", models.CharField(blank=True, max_length=40, null=True)),
            ],
            options={"db_table": "user", "managed": True},
        ),
        migrations.AddField(
            model_name="message",
            name="createdby",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="username",
                to="base.User",
            ),
        ),
    ]
