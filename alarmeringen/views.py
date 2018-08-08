import logging
from pprint import pformat
from datetime import datetime
from rest_framework import viewsets
from alarmeringen.models import Alarmering, CapCode
from alarmeringen.serializers import (AlarmeringSerializer, CapCodeSerializer)

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


def persistAlarmeringen(meldingen, parent=None):
    res = []
    if meldingen is not None:
        logger.info('Ingesting {} meldingen'.format(len(meldingen)))
        for melding in meldingen:
            code = persistAlarmering(melding, parent)
            if code != '':
                res.append(code)
    return res


def persistCaps(caps):
    res = []
    if caps is not None:
        logger.info('Ingesting {} capcodes'.format(len(caps)))
        for cap in caps:
            code = persistCap(cap)
            if code != '':
                res.append(code)
    return res


def persistAlarmering(melding, parent=None):
    res = ''
    logger.debug('{}'.format(pformat(melding)))

    caps = melding.pop('capcodes', '')
    subs = melding.pop('subitems', '')

    # format date DD-MM to YYYY-MM-DD
    dt = datetime.strptime('{}-{}'.format(
        melding.pop('datum'), datetime.now().year), '%d-%m-%Y')
    melding.update({'datum': datetime.strftime(dt, '%Y-%m-%d')})
    melding.update({'parent': parent})

    try:
        obj, created = Alarmering.objects.get_or_create(**melding)
        if caps != '':
            obj.capcodes.add(*persistCaps(caps))
        if subs != '':
            logger.info('Ingesting {} subitems'.format(len(subs)))
            persistAlarmeringen(subs, obj)
        res = obj.id
    except Alarmering.DoesNotExist:
        logger.warning('Does not exist: {}'.format(melding['id']))
        pass
    except Exception as e:
        logger.error('Unknown error: {}'.format(e))

    return res


def persistCap(cap):
    res = ''

    try:
        obj, created = CapCode.objects.get_or_create(**cap)
        logger.debug('Cap code created {}'.format(obj))
        res = obj.capcode
    except CapCode.DoesNotExist:
        logger.warning('Does not exist: {}'.format(cap['capcode']))
        pass
    except Exception as e:
        logger.error('Unknown error: {}'.format(e))
    return res
