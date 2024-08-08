# Generated by Django 5.0.6 on 2024-08-08 04:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0013_ecgdata_expositor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecgdata',
            name='expositor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ecg_data', to='tasks.expositores'),
        ),
    ]
