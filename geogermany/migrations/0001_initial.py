# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('rs', models.CharField(max_length=255, verbose_name='Regional Key')),
                ('ags', models.CharField(max_length=255, verbose_name='Official Municipality Key')),
                ('kind', models.CharField(max_length=255, verbose_name='Kind of Area')),
                ('nuts', models.CharField(max_length=255, verbose_name='NUTS key')),
                ('population', models.IntegerField(null=True)),
                ('area', models.FloatField(default=0.0, verbose_name='Area')),
                ('valid_on', models.DateTimeField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='geometry', geography=True)),
            ],
            options={
                'verbose_name': 'district',
                'verbose_name_plural': 'districts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('rs', models.CharField(max_length=255, verbose_name='Regional Key')),
                ('ags', models.CharField(max_length=255, verbose_name='Official Municipality Key')),
                ('kind', models.CharField(max_length=255, verbose_name='Kind of Area')),
                ('nuts', models.CharField(max_length=255, verbose_name='NUTS key')),
                ('population', models.IntegerField(null=True)),
                ('area', models.FloatField(default=0.0, verbose_name='Area')),
                ('valid_on', models.DateTimeField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='geometry', geography=True)),
                ('part_of', models.ForeignKey(verbose_name='Part of', to='geogermany.District', null=True)),
            ],
            options={
                'verbose_name': 'municipality',
                'verbose_name_plural': 'municipalities',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('rs', models.CharField(max_length=255, verbose_name='Regional Key')),
                ('ags', models.CharField(max_length=255, verbose_name='Official Municipality Key')),
                ('kind', models.CharField(max_length=255, verbose_name='Kind of Area')),
                ('nuts', models.CharField(max_length=255, verbose_name='NUTS key')),
                ('population', models.IntegerField(null=True)),
                ('area', models.FloatField(default=0.0, verbose_name='Area')),
                ('valid_on', models.DateTimeField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='geometry', geography=True)),
            ],
            options={
                'verbose_name': 'state',
                'verbose_name_plural': 'states',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
                ('area', models.FloatField(default=0.0, verbose_name='Area')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='geometry')),
                ('part_of', models.ForeignKey(verbose_name='Part of', to='geogermany.State', null=True)),
            ],
            options={
                'verbose_name': 'zipcode',
                'verbose_name_plural': 'zipcodes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='district',
            name='part_of',
            field=models.ForeignKey(verbose_name='Part of', to='geogermany.State', null=True),
            preserve_default=True,
        ),
    ]
