# Generated by Django 2.1.5 on 2022-03-10 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ltc_main', '0028_auto_20220309_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='slug',
        ),
        migrations.AlterField(
            model_name='grade',
            name='result',
            field=models.IntegerField(max_length=3),
        ),
        migrations.AlterField(
            model_name='teammeeting',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='teammeeting',
            name='weekNumber',
            field=models.IntegerField(choices=[(10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52')], default=10, verbose_name='Week Number'),
        ),
    ]
