# Generated by Django 4.0.5 on 2023-04-13 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_currency_name_cs_currency_name_en_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='month_label',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
