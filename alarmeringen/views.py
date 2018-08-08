import logging
from rest_framework import viewsets

from alarmeringen.models import Alarmering, CapCode, Dienst, Regio
from alarmeringen.serializers import (AlarmeringSerializer, CapCodeSerializer,
                                      DienstSerializer, RegioSerializer)

logger = logging.getLogger('firedept')


class AlarmeringViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Alarmering.objects.filter(parent=None)
    serializer_class = AlarmeringSerializer


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
