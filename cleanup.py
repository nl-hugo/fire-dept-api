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
    capcodes = ['707507','707509','707510','707511','707515','707516']

    n, objs = Alarmering.objects.filter(plaats__in=plaatsen).exclude(capcodes__in=capcodes).delete()
    logger.info('Deleted {} alarmeringen'.format(n))


def run():
    plaatsen = [
        'Abcoude',
        'Amersfoort',
        'Amstelhoek',
        'Baambrugge',
        'Baarn',
        'Barneveld',
        'Bennekom',
        'Blokker',
        'Benschop',
        'Bilthoven',
        'Bosch en duin',
        'Bussum',
        'De bilt',
        'De kwakel',
        'De meern',
        'Den dolder',
        'Eemdijk',
        'Eemnes',
        'Everdingen',
        'Gorinchem',
        'Groenekan',
        'Haarzuilens',
        'Hagestein',
        'Harmelen',
        'Hekendorp',
        'Hernen',
        'Hoevelaken',
        'Hooglanderveen',
        'Houten',
        'Huizen',
        'Hilversum',
        'Hollandsche rading',
        'Hoogland',
        'Kampen',
        'Kamerik',
        'Kedichem',
        'Kortenhoef',
        'Kudelstaart',
        'Kockengen',
        'Lage vuursche',
        'Laren nh',
        'Leerdam',
        'Leusden',
        'Loenersloot',
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
        'Woerden',
        'Woerdense verlaat',
        'Zegveld',
        'Zijderveld',
        'Zwartebroek',
        ''
    ]
    cleanup(plaatsen)


if __name__ == '__main__':
    run()
