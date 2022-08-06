# Generated by Django 3.2.13 on 2022-07-27 13:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("project", "0003_question_question_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="question_author",
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to="auth.user"),
            preserve_default=False,
        ),
    ]
