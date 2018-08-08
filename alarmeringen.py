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


def scrape(params, callback):
    host = 'http://beta.alarmeringdroid.nl/'
    api_url_base = 'api2/find/'
    headers = {'Content-Type': 'application/json', }
    res = None

    api_url = '{0}{1}{2}'.format(host, api_url_base, params)
    api_url = api_url.replace('\'', '\"')
    logger.info('Scrape from {}'.format(api_url))

    response = requests.get(api_url, headers=headers)
    logger.info('Status code {}'.format(response.status_code))

    if response.status_code == 200:
        res = json.loads(response.content.decode('utf-8'))
    callback(res)


def persist_results(res):
    from alarmeringen.persist import persistAlarmeringen

    meldingen = res['meldingen']
    persistAlarmeringen(meldingen)


def run():
    split_char = ','
    regios = '18'
    diensten = '2'

    params = {
        "regios": regios.split(split_char),
        "diensten": diensten.split(split_char),
    }

    scrape(params, persist_results)


if __name__ == '__main__':
    run()
