import logging
from datetime import datetime, timedelta
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from alarmeringen.models import Alarmering, CapCode, Dienst, Regio
from alarmeringen.serializers import (AlarmeringSerializer, CapCodeSerializer,
                                      DienstSerializer, RegioSerializer,
                                      PlaatsSerializer)
#                                      )

logger = logging.getLogger('firedept')


class AlarmeringViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions. 
    Returns objects in the last 365 days.
    """
    queryset = Alarmering.objects.filter(
        parent=None,
        datum__gte=datetime.now() - timedelta(days=365))
    serializer_class = AlarmeringSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('regio', 'dienst', 'capcodes', 'prio1', 'brandinfo',
                     'plaats')


class CapCodeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = CapCode.objects.all()
    serializer_class = CapCodeSerializer
    pagination_class = None


class DienstViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Dienst.objects.all()
    serializer_class = DienstSerializer
    pagination_class = None


class RegioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Regio.objects.all()
    serializer_class = RegioSerializer
    pagination_class = None


class PlaatsViewSet(viewsets.ViewSet):
    """
    Lists plaatsen.
    """
    def list(self, request):
        queryset = Alarmering.objects.order_by('plaats').values('plaats').distinct()
        logger.info(request)
        serializer = PlaatsSerializer(queryset, many=True)
        return Response(serializer.data)
