# Generated by Django 4.1.7 on 2023-03-12 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_like_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
