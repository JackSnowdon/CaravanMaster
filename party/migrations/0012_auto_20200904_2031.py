# Generated by Django 3.1 on 2020-09-04 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
        ('party', '0011_caravan_currently_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caravan',
            name='currently_at',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='caravans', to='world.location'),
        ),
    ]