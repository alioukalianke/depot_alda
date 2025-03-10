# Generated by Django 5.1.6 on 2025-03-02 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genomic_data', '0002_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomicdata',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_genomic_data', to=settings.AUTH_USER_MODEL),
        ),
    ]
