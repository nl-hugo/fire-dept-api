from django.contrib import admin
from .models import Alarmering, Regio, Dienst


class RegioAdmin(admin.ModelAdmin):
    model = Regio


admin.site.register(Regio, RegioAdmin)


class DienstAdmin(admin.ModelAdmin):
    model = Dienst


admin.site.register(Dienst, DienstAdmin)


class CapCodesInline(admin.TabularInline):
    model = Alarmering.capcodes.through
    extra = 0


class CapCodeAdmin(admin.ModelAdmin):
    inlines = [CapCodesInline]


class AlarmeringAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id', 'datum', 'tijd', 'melding',
                                         'parent']}),
        ('Dienst', {'fields': ['dienst', 'prio1', 'grip',
                               'brandinfo', 'details'], 'classes': ['collapse']}),
        ('Locatie', {'fields': ['regio', 'plaats', 'postcode',
                                'straat', 'lat', 'lon'], 'classes': ['collapse']}),
    ]
    inlines = [CapCodesInline, ]
    list_display = ('id', 'datum', 'tijd', 'melding', 'dienst', 'regio', 'plaats',
                    'parent')
    list_filter = ['dienst', 'regio', ]
    search_fields = ['melding', 'plaats', ]


admin.site.register(Alarmering, AlarmeringAdmin)
