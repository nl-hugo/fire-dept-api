import logging
from pprint import pformat
from datetime import datetime
from django.db import IntegrityError

from alarmeringen.models import Alarmering, CapCode, Dienst, Regio


logger = logging.getLogger('firedept')


def persistAlarmeringen(meldingen, parent=None):
    res = []
    if meldingen is not None:
        logger.info('Ingesting {} meldingen'.format(len(meldingen)))
        for melding in meldingen:
            code = persistAlarmering(melding, parent)
            if code != '':
                res.append(code)
    return res


def persistAlarmering(melding, parent=None):
    res = ''
    logger.debug('{}'.format(pformat(melding)))

    caps = melding.pop('capcodes', '')
    subs = melding.pop('subitems', '')

    regio_id = melding.pop('regioid', '')
    regio_oms = melding.pop('regio', '')

    regio = None
    if regio_id != '':
        regio = persistRegio(regio_id, regio_oms)
    melding.update({'regio': regio})

    dienst_id = melding.pop('dienstid', '')
    dienst_oms = melding.pop('dienst', '')

    dienst = None
    if dienst_id != '':
        dienst = persistDienst(dienst_id, dienst_oms)
    melding.update({'dienst': dienst})

    # format date DD-MM to YYYY-MM-DD
    dt = datetime.strptime('{}-{}'.format(
        melding.pop('datum'), datetime.now().year), '%d-%m-%Y')
    melding.update({'datum': datetime.strftime(dt, '%Y-%m-%d')})
    melding.update({'parent': parent})

    try:
        pk = melding.pop('id', '')
        obj, created = Alarmering.objects.get_or_create(pk=pk, defaults=melding)
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


def persistCaps(caps):
    res = []
    if caps is not None:
        logger.info('Ingesting {} capcodes'.format(len(caps)))
        for cap in caps:
            code = persistCap(cap)
            if code != '':
                res.append(code)
    return res


def persistCap(cap):
    res = ''

    try:
        pk = cap.pop('capcode', '')
        obj, created = CapCode.objects.get_or_create(pk=pk, defaults=cap)
        logger.debug('Cap code {} {}'.format(
            obj, 'created' if created else 'updated'))
        res = obj.capcode
    except IntegrityError as e:
        logger.warning('Already exists: {}'.format(pk))
    except Exception as e:
        logger.error('Unknown error {}: {}'.format(pk, e))
    return res


def persistDienst(dienst_id, dienst_oms):
    res = None

    try:
        res, created = Dienst.objects.get_or_create(
            id=dienst_id,
            defaults={'omschrijving': dienst_oms})
        logger.debug('Regio created {}'.format(res))
    except Exception as e:
        logger.error('Unknown error {}: {}'.format(dienst_id, e))
    return res


def persistRegio(regio_id, regio_oms):
    res = None

    try:
        res, created = Regio.objects.get_or_create(
            id=regio_id,
            defaults={'omschrijving': regio_oms})
        logger.debug('Regio created {}'.format(res))
    except Exception as e:
        logger.error('Unknown error {}: {}'.format(regio_id, e))
    return res
