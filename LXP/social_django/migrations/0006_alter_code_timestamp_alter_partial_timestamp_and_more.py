# Generated by Django 4.2.7 on 2025-07-05 04:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_django", "0005_alter_code_timestamp_alter_partial_timestamp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="code",
            name="timestamp",
            field=models.DateTimeField(
                db_index=True, default=datetime.datetime(2025, 7, 5, 10, 2, 19, 116412)
            ),
        ),
        migrations.AlterField(
            model_name="partial",
            name="timestamp",
            field=models.DateTimeField(
                db_index=True, default=datetime.datetime(2025, 7, 5, 10, 2, 19, 116690)
            ),
        ),
        migrations.AlterField(
            model_name="usersocialauth",
            name="created",
            field=models.DateTimeField(
                default=datetime.datetime(2025, 7, 5, 10, 2, 19, 115127)
            ),
        ),
    ]
