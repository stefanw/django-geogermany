from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models


@python_2_unicode_compatible
class GermanGeoArea(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)

    kind = models.CharField(_('Kind of Area'), max_length=255,
        choices=(
            ('state', _('state')),
            ('district', _('district')),
            ('municipality', _('municipality')),
            ('zipcode', _('zipcode')),
        )
    )

    kind_detail = models.CharField(max_length=255, blank=True)

    rs = models.CharField(_('Regional Key'), max_length=255, blank=True)
    ags = models.CharField(_('Official Municipality Key'), max_length=255, blank=True)
    nuts = models.CharField(_('NUTS key'), max_length=255, blank=True)
    population = models.IntegerField(null=True)

    # in Sqm
    area = models.FloatField(_('Area'), default=0.0)
    valid_on = models.DateTimeField(null=True)

    geom = models.MultiPolygonField(_('geometry'), geography=True)

    part_of = models.ForeignKey('self', verbose_name=_('Part of'), null=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('German Geo Area')
        verbose_name_plural = _('German Geo Areas')

    def __str__(self):
        return u'%s (%s)' % (self.name, self.pk)

    def calculate_area(self):
        self.geom.transform(102013)
        self.area = self.geom.area
        self.geom.transform(4326)
        return self.area


def get_manager(kind_filter):
    class CustomGeoManager(models.GeoManager):
        def get_queryset(self):
            return super(CustomGeoManager, self).get_queryset().filter(kind=kind_filter)

    return CustomGeoManager()


class State(GermanGeoArea):
    objects = get_manager('state')

    class Meta:
        proxy = True
        verbose_name = _('state')
        verbose_name_plural = _('states')


class District(GermanGeoArea):
    objects = get_manager('district')

    class Meta:
        proxy = True
        verbose_name = _('district')
        verbose_name_plural = _('districts')


class Municipality(GermanGeoArea):
    objects = get_manager('municipality')

    class Meta:
        proxy = True
        verbose_name = _('municipality')
        verbose_name_plural = _('municipalities')


class ZipCode(GermanGeoArea):
    objects = get_manager('zipcode')

    class Meta:
        proxy = True
        verbose_name = _('zipcode')
        verbose_name_plural = _('zipcodes')
