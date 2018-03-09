# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('scheduled_time', models.DateTimeField(null=True)),
                ('reason', models.CharField(max_length=100, null=True)),
                ('checked', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['scheduled_time'],
            },
        ),
        migrations.CreateModel(
            name='CheckIns',
            fields=[
                ('appointment_id', models.IntegerField(serialize=False, primary_key=True)),
                ('check_in_time', models.DateTimeField(auto_now_add=True)),
                ('meet_time', models.DateTimeField(null=True)),
                ('completed', models.BooleanField(default=False)),
                ('status', models.CharField(default=0, max_length=9, choices=[(b'checked_in', b'Checked In'), (b'arrived', b'Arrived'), (b'completed', b'Complete')])),
            ],
            options={
                'ordering': ['-meet_time'],
            },
        ),
        migrations.CreateModel(
            name='Configure',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('dr_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('salt_ssn', models.CharField(max_length=100)),
                ('photo', models.CharField(max_length=500)),
                ('user', models.ForeignKey(to='drchrono.Configure')),
            ],
        ),
        migrations.AddField(
            model_name='checkins',
            name='user',
            field=models.ForeignKey(to='drchrono.Configure'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(to='drchrono.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='user',
            field=models.ForeignKey(to='drchrono.Configure'),
        ),
    ]
