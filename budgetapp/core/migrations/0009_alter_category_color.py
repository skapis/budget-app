# Generated by Django 4.0.5 on 2023-04-01 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_category_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
