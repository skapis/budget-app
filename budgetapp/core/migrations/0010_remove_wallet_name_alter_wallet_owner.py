# Generated by Django 4.0.5 on 2023-04-03 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_alter_category_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='name',
        ),
        migrations.AlterField(
            model_name='wallet',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
