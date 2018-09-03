import os
import json
import requests
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


def cleanup(plaatsen):
    from alarmeringen.models import Alarmering

    n, objs = Alarmering.objects.filter(plaats__in=plaatsen).delete()
    logger.info('Deleted {} alarmeringen'.format(n))


def run():
    plaatsen = [
        'Baarn',
        'Benschop',
        'De kwakel',
        'De meern',
        'Everdingen',
        'Haarzuilens',
        'Hagestein',
        'Harmelen',
        'Hekendorp',
        'Hernen',
        'Hoevelaken',
        'Hooglanderveen',
        'Houten',
        'Huizen',
        'Kamerik',
        'Kockengen',
        'Lage vuursche',
        'Laren nh',
        'Leusden',
        'Lexmond',
        'Linschoten',
        'Loenen aan de vecht',
        'Lopik',
        'Maarssen',
        'Maartensdijk',
        'Mijdrecht',
        'Montfoort',
        'Nederhorst den berg',
        'Nederland',
        'Neer',
        'Nieuwegein',
        'Nieuwerbrug',
        'Nieuwersluis',
        'Nigtevecht',
        'Odijk',
        'Oud zuilen',
        'Ouderkerk aan de amstel',
        'Oudewater',
        'Schalkwijk',
        'Soest',
        'Soesterberg',
        '\'t goy',
        'Tienhoven ut',
        'Uithoorn',
        'Utrecht',
        'Vianen ut',
        'Vinkeveen',
        'Vleuten',
        'Vreeland',
        'Waverveen',
        'Wilnis',
        'Zegveld',
        'Zijderveld',
        ''
    ]
    cleanup(plaatsen)


if __name__ == '__main__':
    run()
