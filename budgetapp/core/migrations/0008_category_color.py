# Generated by Django 4.0.5 on 2023-04-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
