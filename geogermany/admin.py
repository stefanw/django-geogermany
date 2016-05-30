from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import (GermanGeoArea, State, District, Municipality, Borough,
                    ZipCode)


class GeoAreaAdmin(LeafletGeoAdmin):
    search_fields = ['name', 'ags', 'rs']
    list_display = ('name', 'kind')
    list_filter = ('kind',)
    raw_id_fields = ('part_of',)


class StateAdmin(GeoAreaAdmin):
    pass


class DistrictAdmin(GeoAreaAdmin):
    pass


class MunicipalityAdmin(GeoAreaAdmin):
    pass


class BoroughAdmin(GeoAreaAdmin):
    pass


class ZipCodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Borough, BoroughAdmin)
admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(GermanGeoArea, GeoAreaAdmin)
