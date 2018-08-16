import logging
from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from alarmeringen.models import Alarmering, CapCode, Dienst, Regio
from alarmeringen.filters import AlarmeringFilter
from alarmeringen.serializers import (AlarmeringSerializer, CapCodeSerializer,
                                      DienstSerializer, RegioSerializer,
                                      PlaatsSerializer)

logger = logging.getLogger('firedept')


class AlarmeringViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions. 
    Returns objects in the last 365 days.
    """
    queryset = Alarmering.objects.filter(
#        parent=None,
        datum__gte=datetime.now() - timedelta(days=365))
    serializer_class = AlarmeringSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = AlarmeringFilter


class CapCodeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CapCode.objects.annotate(num=Count('alarmeringen')).filter(
        num__gt=0)
    serializer_class = CapCodeSerializer
    pagination_class = None


class DienstViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Dienst.objects.annotate(num=Count('alarmeringen')).filter(
        num__gt=0)
    serializer_class = DienstSerializer
    pagination_class = None


class RegioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Regio.objects.annotate(num=Count('alarmeringen')).filter(
        num__gt=0)
    serializer_class = RegioSerializer
    pagination_class = None


class PlaatsViewSet(viewsets.ViewSet):
    """
    Lists plaatsen.
    """
    def list(self, request):
        queryset = Alarmering.objects.order_by('plaats').annotate(
                num=Count('id')
            ).filter(
                num__gt=0
            ).exclude(
                plaats__exact=''
            ).values('plaats').distinct()
        logger.info(request)
        serializer = PlaatsSerializer(queryset, many=True)
        return Response(serializer.data)
