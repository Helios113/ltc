# Generated by Django 2.1.5 on 2022-02-22 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ltc_main', '0022_teammeeting_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammeeting',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
