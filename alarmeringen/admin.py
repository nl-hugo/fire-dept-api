from django.contrib import admin
from .models import Alarmering, Regio


class RegioAdmin(admin.ModelAdmin):
    model = Regio


admin.site.register(Regio, RegioAdmin)


class CapCodesInline(admin.TabularInline):
    model = Alarmering.capcodes.through
    extra = 0


class CapCodeAdmin(admin.ModelAdmin):
    inlines = [CapCodesInline]


class AlarmeringAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id', 'datum', 'tijd', 'melding',
                                         'parent']}),
        ('Dienst', {'fields': ['dienstid', 'dienst', 'prio1', 'grip',
                               'brandinfo', 'details'], 'classes': ['collapse']}),
        ('Locatie', {'fields': ['regio', 'plaats', 'postcode',
                                'straat', 'lat', 'lon'], 'classes': ['collapse']}),
    ]
    inlines = [CapCodesInline, ]
    list_display = ('id', 'datum', 'tijd', 'melding', 'regio', 'plaats',
                    'parent')
    list_filter = ['dienst', ]
    search_fields = ['melding', 'plaats', ]


admin.site.register(Alarmering, AlarmeringAdmin)
