from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models


class GeoMixin(object):
    def calculate_area(self):
        self.geom.transform(102013)
        self.area = self.geom.area
        self.geom.transform(4326)


@python_2_unicode_compatible
class GermanGeoArea(GeoMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)
    rs = models.CharField(_('Regional Key'), max_length=255)
    ags = models.CharField(_('Official Municipality Key'), max_length=255)
    kind = models.CharField(_('Kind of Area'), max_length=255)
    nuts = models.CharField(_('NUTS key'), max_length=255)

    population = models.IntegerField(null=True)

    # in Sqm
    area = models.FloatField(_('Area'), default=0.0)
    valid_on = models.DateTimeField(null=True)

    geom = models.MultiPolygonField(_('geometry'), geography=True)

    objects = models.GeoManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class State(GermanGeoArea):
    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')


class District(GermanGeoArea):
    part_of = models.ForeignKey(State, verbose_name=_('Part of'), null=True)

    class Meta:
        verbose_name = _('district')
        verbose_name_plural = _('districts')


class Municipality(GermanGeoArea):
    part_of = models.ForeignKey(District, verbose_name=_('Part of'), null=True)

    class Meta:
        verbose_name = _('municipality')
        verbose_name_plural = _('municipalities')


@python_2_unicode_compatible
class ZipCode(GeoMixin, models.Model):
    name = models.CharField(_('Name'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=255)

    area = models.FloatField(_('Area'), default=0.0)
    geom = models.MultiPolygonField(_('geometry'))
    part_of = models.ForeignKey(State, verbose_name=_('Part of'), null=True)

    objects = models.GeoManager()

    class Meta:
        verbose_name = _('zipcode')
        verbose_name_plural = _('zipcodes')

    def __str__(self):
        return self.name
