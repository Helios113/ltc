# Generated by Django 2.1.5 on 2022-03-15 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ltc_main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='geoUri',
            field=models.CharField(default='VPC5+XX Glasgow', max_length=128),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
