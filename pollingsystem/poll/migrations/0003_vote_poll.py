# Generated by Django 5.0.7 on 2024-07-13 12:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='poll',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='poll.poll'),
            preserve_default=False,
        ),
    ]
