# Generated by Django 4.2.3 on 2024-06-11 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chicken_expert_app', '0004_interaction_created_at_interaction_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='location_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
