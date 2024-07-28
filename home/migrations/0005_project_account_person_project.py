# Generated by Django 5.0.7 on 2024-07-25 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_department_dept_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('company', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.PositiveSmallIntegerField()),
                ('DoJ', models.DateField()),
                ('person', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='Account', to='home.person')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='project',
            field=models.ManyToManyField(related_name='child_three', to='home.project'),
        ),
    ]