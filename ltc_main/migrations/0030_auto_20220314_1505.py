# Generated by Django 2.1.5 on 2022-03-14 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ltc_main', '0029_auto_20220310_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='type',
            field=models.CharField(choices=[('Lecture', 'Lecture'), ('Tutorial', 'Tutorial'), ('Lab', 'Lab')], default='Lecture', max_length=64),
        ),
        migrations.AlterField(
            model_name='grade',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Assignment'),
        ),
        migrations.AlterField(
            model_name='teammeeting',
            name='weekNumber',
            field=models.IntegerField(choices=[(11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52')], default=11, verbose_name='Week Number'),
        ),
    ]
