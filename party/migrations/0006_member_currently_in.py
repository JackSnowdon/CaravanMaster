# Generated by Django 3.1 on 2020-09-02 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0005_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='currently_in',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='crew', to='party.caravan'),
        ),
    ]
