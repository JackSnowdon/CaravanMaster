# Generated by Django 3.1 on 2020-09-02 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('party', '0003_auto_20200902_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caravan',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cav', to='party.avatar'),
        ),
    ]
