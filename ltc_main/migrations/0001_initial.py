# Generated by Django 2.1.5 on 2022-03-15 02:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import eventtools.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('detail', models.TextField(blank=True, max_length=512, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=128, unique=True)),
                ('name', models.CharField(default='default', max_length=128)),
                ('description', models.TextField(default='default', max_length=512)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('photo', models.TextField()),
                ('prerequisite', models.ManyToManyField(blank=True, to='ltc_main.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('course', models.ManyToManyField(to='ltc_main.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=512, null=True)),
                ('location', models.CharField(max_length=128)),
                ('type', models.CharField(choices=[('Lecture', 'Lecture'), ('Tutorial', 'Tutorial'), ('Lab', 'Lab')], default='Lecture', max_length=64)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, eventtools.models.OccurrenceMixin),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(default=0)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Assignment')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('type', models.CharField(choices=[('Professor', 'Professor'), ('Teaching assistant', 'Teaching assistant'), ('Administrator', 'Administrator')], default='Professor', max_length=64)),
                ('courses', models.ManyToManyField(to='ltc_main.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('courses', models.ManyToManyField(blank=True, to='ltc_main.Course')),
                ('degree', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Degree')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMeeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('slug', models.SlugField(blank=True, editable=False, null=True, unique=True)),
                ('weekNumber', models.IntegerField(choices=[(11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'), (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'), (33, '33'), (34, '34'), (35, '35'), (36, '36'), (37, '37'), (38, '38'), (39, '39'), (40, '40'), (41, '41'), (42, '42'), (43, '43'), (44, '44'), (45, '45'), (46, '46'), (47, '47'), (48, '48'), (49, '49'), (50, '50'), (51, '51'), (52, '52')], default=11, verbose_name='Week Number')),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(db_index=True, verbose_name='start')),
                ('end', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='end')),
                ('repeat', eventtools.models.ChoiceTextField(blank=True, choices=[('RRULE:FREQ=DAILY', 'Daily'), ('RRULE:FREQ=WEEKLY', 'Weekly'), ('RRULE:FREQ=MONTHLY', 'Monthly'), ('RRULE:FREQ=YEARLY', 'Yearly')], default='', verbose_name='repeat')),
                ('repeat_until', models.DateField(blank=True, null=True, verbose_name='repeat_until')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Event')),
            ],
            options={
                'ordering': ('start', 'end'),
                'abstract': False,
            },
            bases=(models.Model, eventtools.models.OccurrenceMixin),
        ),
        migrations.AddField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Student'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ltc_main.Course'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='ltc_main.TimeSlot'),
        ),
    ]
