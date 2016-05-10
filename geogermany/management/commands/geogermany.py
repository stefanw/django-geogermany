import os

from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from django.contrib.gis.geos.error import GEOSException

from slugify import slugify

from ...models import GermanGeoArea, State, District, Municipality, ZipCode


class Command(BaseCommand):
    help = "geogermany"

    def add_arguments(self, parser):
        parser.add_argument('command', help='Subcommand')
        parser.add_argument('base_path', help='Add base path')

    def handle(self, *args, **options):
        getattr(self, options['command'])(**options)

    def load(self, **options):
        base_path = options['base_path']
        self.stdout.write("\nState\n")
        self.load_by_path(State, base_path, 'bundeslaender.shp')
        self.stdout.write("\nDistrict\n")
        self.load_by_path(District, base_path, 'landkreise.shp')
        self.stdout.write("\nMunicipality\n")
        self.load_by_path(Municipality, base_path, 'gemeinden.shp')
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
            self.stdout.write('%.2f%%\r' % (i / count * 100), ending='')
            name = feature['GEN'].as_string()
            kind_detail = feature['DES'].as_string()
            slug = slugify(u'%s %s' % (kind_detail, name))

            geom = mapping.feature_kwargs(feature)['geom']

            # validity = feature['WSK'].as_string()
            # if validity:
            #     naive = datetime.strptime(validity, '%Y/%m/%d')
            #     validity = pytz.timezone("Europe/Berlin").localize(naive, is_dst=None)
            # else:
            validity = None
            kind = klass.__name__.lower()

            klass.objects.get_or_create(slug=slug, kind=kind, defaults={
                'name': name,
                'rs': feature['RS'].as_string(),
                'ags': feature['AGS'].as_string() if 'AGS' in feature else '',
                'kind': kind,
                'kind_detail': kind_detail,
                'nuts': feature['NUTS'].as_string() if 'NUTS' in feature else '',
                'population': (feature['EWZ_W'].as_int() + feature['EWZ_M'].as_int()) if 'EWZ_W' in feature else None,
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
                'area': feature.geom.area,
                'kind': 'zipcode'
            })

    def create_hierarchy(self, *args, **options):
        matches = [
            ('district', 'state'),
            ('municipality', 'district'),
            ('zipcode', 'state')
        ]
        for small, big in matches:
            for small_obj in GermanGeoArea.objects.filter(kind=small,
                                                          part_of__isnull=True):
                print('Trying', small_obj)
                try:
                    big_objs = GermanGeoArea.objects.filter(kind=big, geom__covers=small_obj.geom.point_on_surface)
                except GEOSException:
                    big_objs = GermanGeoArea.objects.filter(kind=big, geom__covers=small_obj.geom.centroid)
                if not big_objs:
                    big_objs = GermanGeoArea.objects.filter(kind=big, geom__intersects=small_obj.geom)
                if len(big_objs) == 1:
                    small_obj.part_of = big_objs[0]
                    small_obj.save()
                    print(small_obj, 'assigned', big_objs[0])
                elif len(big_objs) == 0:
                    print(small_obj, "0", big)
                else:
                    print(small_obj, 'too many', big_objs)

    def calculate_area(self, *args, **options):
        for obj in GermanGeoArea.objects.all():
            obj.calculate_area()
            obj.save()
