# Generated by Django 2.1.5 on 2022-02-20 17:56

from django.db import migrations, models
import django.db.models.deletion
import eventtools.models


class Migration(migrations.Migration):

    dependencies = [
        ('ltc_main', '0003_auto_20220220_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeslot',
            options={'ordering': ('start', 'end')},
        ),
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time_slot',
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='events',
            field=models.ManyToManyField(to='ltc_main.TimeSlot'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='end',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='end'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='event',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeslot',
            name='repeat',
            field=eventtools.models.ChoiceTextField(blank=True, choices=[('RRULE:FREQ=DAILY', 'Daily'), ('RRULE:FREQ=WEEKLY', 'Weekly'), ('RRULE:FREQ=MONTHLY', 'Monthly'), ('RRULE:FREQ=YEARLY', 'Yearly')], default='', verbose_name='repeat'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='repeat_until',
            field=models.DateField(blank=True, null=True, verbose_name='repeat_until'),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='start',
            field=models.DateTimeField(db_index=True, default=None, verbose_name='start'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='day',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='timeslot',
            name='time',
        ),
    ]
