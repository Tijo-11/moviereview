# Generated by Django 5.1.5 on 2025-02-08 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='watchAgain',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')]),
        ),
    ]
