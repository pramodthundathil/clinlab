# Generated by Django 5.0.7 on 2024-08-02 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0008_order_approval_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='test_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='ComprehensiveTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('specimen', models.CharField(blank=True, max_length=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('availability', models.BooleanField(default=True)),
                ('tests', models.ManyToManyField(to='Clinic.testtype')),
            ],
        ),
    ]
