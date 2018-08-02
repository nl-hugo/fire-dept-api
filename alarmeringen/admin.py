from django.contrib import admin
from .models import Alarmering


class CapCodesInline(admin.TabularInline):
    model = Alarmering.capcodes.through
    extra = 0


class CapCodeAdmin(admin.ModelAdmin):
    inlines = [CapCodesInline]


class SubitemsInline(admin.TabularInline):
    model = Alarmering.subitems.through
    fk_name = 'from_alarmering'
    extra = 0


class AlarmeringAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['id', 'datum', 'tijd', 'melding']}),
        ('Dienst', {'fields': ['dienstid', 'dienst', 'prio1', 'grip', 'brandinfo', 'details'], 'classes': ['collapse']}),
        ('Locatie', {'fields': ['regioid', 'regio', 'plaats', 'postcode', 'straat', 'lat', 'lon'], 'classes': ['collapse']}),
    ]
    inlines = [CapCodesInline, SubitemsInline]
    list_display = ('id', 'datum', 'tijd', 'melding', 'regio', 'plaats')
    list_filter = ['dienst', 'regio']
    search_fields = ['melding', 'regio', 'plaats']


admin.site.register(Alarmering, AlarmeringAdmin)
