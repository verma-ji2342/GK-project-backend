# Generated by Django 5.0.7 on 2024-07-22 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_state_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_name',
            field=models.CharField(max_length=35),
        ),
    ]
