# Generated by Django 5.0.7 on 2024-07-25 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('normal_range', models.CharField(default=' ', max_length=100)),
                ('unit', models.CharField(max_length=50)),
                ('Interpertaion_description', models.TextField(default='', null=True)),
            ],
        ),
    ]
