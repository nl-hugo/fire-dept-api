import logging
from pprint import pformat
from datetime import datetime
from alarmeringen.models import Alarmering, CapCode

logger = logging.getLogger('firedept')


def persistAlarmeringen(meldingen):
    res = []
    if meldingen is not None:
        logger.info('Ingesting {} meldingen'.format(len(meldingen)))
        for melding in meldingen:
            code = persistAlarmering(melding)
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


def persistAlarmering(melding):
    res = ''
    logger.debug('{}'.format(pformat(melding)))

    caps = melding.pop('capcodes', '')
    subs = melding.pop('subitems', '')

    # format date DD-MM to YYYY-MM-DD
    dt = datetime.strptime('{}-{}'.format(
        melding.pop('datum'), datetime.now().year), '%d-%M-%Y')
    melding.update({'datum': datetime.strftime(dt, '%Y-%M-%d')})

    try:
        obj, created = Alarmering.objects.get_or_create(**melding)
        if caps != '':
            obj.capcodes.add(*persistCaps(caps))
        if subs != '':
            obj.subitems.add(*persistAlarmeringen(subs))
        res = obj.id
    except Alarmering.DoesNotExist:
        logger.warning('Does not exist: {}'.format(melding['code']))
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
