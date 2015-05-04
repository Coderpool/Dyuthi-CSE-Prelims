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
            name='Event',
            fields=[
                ('eventId', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('durationInMins', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=1000)),
                ('option_B', models.CharField(max_length=1000)),
                ('option_C', models.CharField(max_length=1000)),
                ('option_D', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(null=True, blank=True)),
                ('startTime', models.DateTimeField(null=True, blank=True)),
                ('negatives', models.PositiveIntegerField(null=True, blank=True)),
                ('deltaSec', models.PositiveIntegerField(null=True, blank=True)),
                ('deltaMicro', models.PositiveIntegerField(null=True, blank=True)),
                ('event', models.ForeignKey(to='exam.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('setId', models.AutoField(serialize=False, primary_key=True)),
                ('setname', models.CharField(max_length=200)),
                ('numberOfQuestions', models.IntegerField()),
                ('positiveMarks', models.PositiveIntegerField()),
                ('negativeMarks', models.PositiveIntegerField()),
                ('test', models.ForeignKey(to='exam.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='questions',
            name='set',
            field=models.ForeignKey(to='exam.Set'),
            preserve_default=True,
        ),
    ]
