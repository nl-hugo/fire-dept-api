import os
import logging
import django

__version__ = '0.0.1'

#
# Initialize logging
#
logger = logging.getLogger('firedept')
logger.info('Initialized {} version {}'.format(__name__, __version__))

#
# Django setup
#
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firedept.settings')
django.setup()
logger.info('Django version {}'.format(django.__version__))


def cleanup():
    from alarmeringen.models import Alarmering, CapCode
    capcodes = ['707507', '707508', '707509', '707510', '707511', '707512', '707513', '707514', '707515', '707516']

    n, objs = Alarmering.objects.exclude(capcodes__in=capcodes).delete()
    logger.info('Deleted {} alarmeringen'.format(n))

    n, objs = CapCode.objects.exclude(capcode__in=capcodes).delete()
    logger.info('Deleted {} capcodes'.format(n))


def run():
    cleanup()


if __name__ == '__main__':
    run()
