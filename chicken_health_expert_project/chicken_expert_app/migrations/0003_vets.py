# Generated by Django 4.2.3 on 2024-05-27 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chicken_expert_app', '0002_alter_interaction_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
    ]