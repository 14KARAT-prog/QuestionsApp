# Generated by Django 3.2.13 on 2022-07-08 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project", "0002_rename_question_test_question_question_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="question_title",
            field=models.CharField(default="hello", max_length=50),
            preserve_default=False,
        ),
    ]
