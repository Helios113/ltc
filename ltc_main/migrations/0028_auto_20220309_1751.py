# Generated by Django 2.1.5 on 2022-03-09 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ltc_main', '0027_auto_20220309_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
