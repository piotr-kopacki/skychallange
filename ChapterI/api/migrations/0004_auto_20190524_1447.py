# Generated by Django 2.2.1 on 2019-05-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("api", "0003_auto_20190524_1446")]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="answer",
            field=models.TextField(blank=True, null=True),
        )
    ]
