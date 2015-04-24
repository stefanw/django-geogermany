import os
from datetime import datetime

import pytz

from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping

from slugify import slugify

from ...models import State, District, Municipality, ZipCode


class Command(BaseCommand):
    help = "geogermany"

    def handle(self, *args, **options):
        if hasattr(self, args[0]):
            getattr(self, args[0])(*args[1:], **options)
        else:
            print "Sub-Command not found"

    def load(self, *args, **options):
        base_path = args[0]
        self.stdout.write("\nState\n")
        self.load_by_path(State, base_path, 'VG250_LAN.shp')
        self.stdout.write("\nDistrict\n")
        self.load_by_path(District, base_path, 'VG250_KRS.shp')
        self.stdout.write("\nMunicipality\n")
        self.load_by_path(Municipality, base_path, 'VG250_GEM.shp')
        self.stdout.write("\nZipCode\n")
        self.load_zip(ZipCode, base_path, 'plz.geojson')

    def load_by_path(self, klass, base_path, filename):
        path = os.path.abspath(os.path.join(base_path, filename))
        ds = DataSource(path)
        mapping = LayerMapping(klass, ds, {'geom': 'POLYGON'})
        self.load_bkg(ds, klass, mapping)

    def load_bkg(self, ds, klass, mapping):
        layer = ds[0]
        count = float(len(layer))
        for i, feature in enumerate(layer):
            if feature['GF'].as_int() != 4:
                continue
            self.stdout.write('%.2f%%\r' % (i / count * 100), ending='')
            name = feature['GEN'].as_string()
            slug = slugify(name)

            geom = mapping.feature_kwargs(feature)['geom']

            validity = feature['WSK'].as_string()
            if validity:
                naive = datetime.strptime(validity, '%Y/%m/%d')
                validity = pytz.timezone("Europe/Berlin").localize(naive, is_dst=None)
            else:
                validity = None
            klass.objects.get_or_create(slug=slug, defaults={
                'name': name,
                'rs': feature['RS'].as_string(),
                'ags': feature['AGS'].as_string(),
                'kind': feature['BEZ'].as_string(),
                'nuts': feature['NUTS'].as_string(),
                'population': feature['EWZ'].as_int(),
                'geom': geom,
                'area': feature.geom.area,
                'valid_on': validity
            })

    def load_zip(self, klass, base_path, filename):
        path = os.path.abspath(os.path.join(base_path, filename))
        ds = DataSource(path)
        mapping = LayerMapping(klass, ds, {'geom': 'geometry'})
        layer = ds[0]
        for feature in layer:
            name = feature['plz'].as_string()
            slug = name
            geom = mapping.feature_kwargs(feature)['geom']
            klass.objects.get_or_create(slug=slug, defaults={
                'name': name,
                'geom': geom,
                'area': feature.geom.area
            })

    def create_hierarchy(self, *args, **options):
        for district in District.objects.all():
            state = State.objects.filter(geom__covers=district.geom.centroid)
            if len(state) == 1:
                district.part_of = state[0]
                district.save()
            elif len(state) == 0:
                print district, "0 states"
            else:
                print district, state

        for muni in Municipality.objects.all():
            dis = District.objects.filter(geom__covers=muni.geom.centroid)
            if len(dis) == 1:
                muni.part_of = dis[0]
                muni.save()
            elif len(dis) == 0:
                print muni, "0 districts"
            else:
                print muni, dis

        for zipcode in ZipCode.objects.all():
            print zipcode
            state = State.objects.filter(geom__covers=zipcode.geom.centroid)
            if len(state) == 1:
                zipcode.part_of = state[0]
                zipcode.save()
            elif len(state) == 0:
                print zipcode, "0 states"
            else:
                print zipcode, state

    def calculate_area(self, *args, **options):
        for klass in (State, Municipality, District, ZipCode):
            for obj in klass.objects.all():
                obj.calculate_area()
                obj.save()
