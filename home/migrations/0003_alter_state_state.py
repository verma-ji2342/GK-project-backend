# Generated by Django 5.0.7 on 2024-07-22 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_state_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='state',
            field=models.CharField(max_length=40),
        ),
    ]
