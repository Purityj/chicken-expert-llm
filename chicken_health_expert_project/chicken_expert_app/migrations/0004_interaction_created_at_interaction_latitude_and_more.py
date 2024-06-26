# Generated by Django 4.2.3 on 2024-05-31 18:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chicken_expert_app', '0003_vets'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='interaction',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interaction',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
