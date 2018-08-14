from django_filters import FilterSet, DateFromToRangeFilter
from alarmeringen.models import Alarmering

class AlarmeringFilter(FilterSet):
    datum = DateFromToRangeFilter()

    class Meta:
        model = Alarmering
        fields = ['regio', 'dienst', 'capcodes', 'prio1', 'brandinfo',
                     'plaats', 'datum']
