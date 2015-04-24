from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import State, District, Municipality, ZipCode


class GeoAreaAdmin(LeafletGeoAdmin):
    search_fields = ['name']
    list_display = ('name', 'kind')


class StateAdmin(GeoAreaAdmin):
    pass


class DistrictAdmin(GeoAreaAdmin):
    pass


class MunicipalityAdmin(GeoAreaAdmin):
    pass


class ZipCodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
