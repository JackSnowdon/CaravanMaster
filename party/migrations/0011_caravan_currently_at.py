# Generated by Django 3.1 on 2020-09-04 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
        ('party', '0010_memberbase_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='caravan',
            name='currently_at',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='games', to='world.location'),
        ),
    ]
