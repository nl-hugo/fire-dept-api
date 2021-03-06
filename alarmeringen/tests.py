import json
from datetime import datetime
from os import path
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from alarmeringen.models import Alarmering, CapCode, Dienst, Regio
from alarmeringen.persist import (persistAlarmeringen, persistCaps,
                                  persistDienst, persistRegio)

class PersistDienstTests(TestCase):
    fixtures = ['dienst']

    def test_persist_dienst(self):
        """
        Diensten should be persisted correctly
        """
        dienst = persistDienst('1', 'new')
        self.assertEqual(Dienst.objects.count(), 3)
        self.assertEqual(Dienst.objects.get(id='1'), dienst)

    def test_update_dienst(self):
        """
        Diensten should be updated correctly
        """
        persistDienst('2', 'updated')
        self.assertEqual(Dienst.objects.count(), 2)
        self.assertEqual(Dienst.objects.get(id='2').omschrijving, 'Brandweer')


class PersistRegioTests(TestCase):
    fixtures = ['regio']

    def test_persist_regio(self):
        """
        Regio's should be persisted correctly
        """
        regio = persistRegio('1', 'new')
        self.assertEqual(Regio.objects.count(), 3)
        self.assertEqual(Regio.objects.get(id='1'), regio)

    def test_update_regio(self):
        """
        Regio's should be updated correctly
        """
        persistRegio('18', 'updated')
        self.assertEqual(Regio.objects.count(), 2)
        self.assertEqual(Regio.objects.get(id='18').omschrijving, 'Utrecht')


class PersistCapsTests(TestCase):
    fixtures = ['capcode']

    def test_persist_empty_caps(self):
        """
        Empty cap codes should return an empty list
        """
        res = persistCaps(None)
        self.assertEqual(res, [])
        self.assertEqual(CapCode.objects.count(), 1)

    def test_persist_caps(self):
        """
        Caps should be persisted correctly
        """
        caps = [{
            "capcode": "707000",
            "omschrijving": "Monitorcode"
        }]
        res = persistCaps(caps)
        self.assertEqual(len(res), 1)
        self.assertEqual(CapCode.objects.count(), 2)
        self.assertEqual(CapCode.objects.first().capcode, res[0])

    def test_update_caps(self):
        """
        Caps should be updated correctly
        """
        caps = [{
            "capcode": "707001",
            "omschrijving": "Monitorcode"
        }]
        persistCaps(caps)
        self.assertEqual(CapCode.objects.count(), 1)
        self.assertEqual(CapCode.objects.first().omschrijving, 'Algemeen')


class PersistAlarmeringenTests(TestCase):

    def setUp(self):
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(
                basepath, 'fixtures', 'response.json'))

        with open(filepath, 'r') as f:
            self.alarmeringen = json.load(f)['meldingen']

    def test_persist_empty_alarmeringen(self):
        """
        Empty alarmeringen should return an empty list
        """
        res = persistAlarmeringen(None)
        self.assertEqual(res, [])
        self.assertEqual(Alarmering.objects.count(), 0)

    def test_persist_alarmeringen(self):
        """
        Alarmeringen should be persisted correctly
        """
        res = persistAlarmeringen(self.alarmeringen)
        self.assertEqual(len(res), 2)
        self.assertEqual(Alarmering.objects.count(), 3)
        self.assertEqual(Regio.objects.count(), 1)
        self.assertEqual(CapCode.objects.count(), 7)

    def test_persist_alarmering(self):
        """
        Alarmeringen should be persisted correctly
        """
        persistAlarmeringen(self.alarmeringen)

        s = Alarmering.objects.get(pk='13148251')
        self.assertEqual(s.brandinfo, 'hulpverlening')
        self.assertEqual(s.plaats, 'Abcoude')
        self.assertEqual(datetime.strftime(s.datum, '%Y-%m-%d'), '2018-08-01')
        self.assertEqual(s.capcodes.count(), 4)

    def test_persist_alarmering_subitems(self):
        """
        Subitems should be persisted correctly
        """
        persistAlarmeringen(self.alarmeringen)

        p = Alarmering.objects.get(pk='13148251')
        self.assertEqual(p.parent, None)
        self.assertEqual(p.subitems.count(), 1)

        c = Alarmering.objects.get(pk='13148387')
        self.assertEqual(c.parent, p)
        self.assertEqual(c.subitems.count(), 0)

    def test_persist_alarmering_delayed_subitem(self):
        """
        Delayed subitems should be persisted correctly
        """
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(
                basepath, 'fixtures', 'response_delayed.json'))

        with open(filepath, 'r') as f:
            self.delayed = json.load(f)['meldingen']

        persistAlarmeringen(self.alarmeringen)
        self.assertEqual(Alarmering.objects.count(), 3)
        with self.assertRaises(Alarmering.DoesNotExist):
            Alarmering.objects.get(pk='13199999')

        persistAlarmeringen(self.delayed)
        self.assertEqual(Alarmering.objects.count(), 4)
        self.assertEqual(Alarmering.objects.get(pk='13199999').capstring, 'delayed subitem')

class DienstViewSetTests(APITestCase):
    fixtures = ['alarmeringen', 'regio', 'dienst']

    def test_view_with_alarmeringen(self):
        """
        View should return diensten with alarmeringen only
        """
        response = self.client.get('/diensten/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_view_detail_with_alarmeringen(self):
        """
        View should return the correct description
        """
        response = self.client.get('/diensten/2/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['omschrijving'], 'Brandweer')

    def test_view_detail_with_no_alarmeringen(self):
        """
        Diensten without alarmeringen should not be returned
        """
        response = self.client.get('/diensten/99/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RegioViewSetTests(APITestCase):
    fixtures = ['alarmeringen', 'regio', 'dienst']

    def test_view_with_alarmeringen(self):
        """
        View should return regios with alarmeringen only
        """
        response = self.client.get('/regios/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_view_detail_with_alarmeringen(self):
        """
        View should return the correct description
        """
        response = self.client.get('/regios/18/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['omschrijving'], 'Utrecht')

    def test_view_detail_with_no_alarmeringen(self):
        """
        Regios without alarmeringen should not be returned
        """
        response = self.client.get('/regios/99/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CapCodeViewSetTests(APITestCase):
    fixtures = ['alarmeringen', 'regio', 'dienst']

    def test_view_with_alarmeringen(self):
        """
        View should return capcodes with alarmeringen only
        """
        response = self.client.get('/capcodes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_view_detail_with_alarmeringen(self):
        """
        View should return the correct description
        """
        response = self.client.get('/capcodes/706001/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['omschrijving'], 'Monitorcode')

    def test_view_detail_with_no_alarmeringen(self):
        """
        Capcodes without alarmeringen should not be returned
        """
        response = self.client.get('/capcodes/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AlarmeringEmptyViewSetTests(APITestCase):

    def test_index_view_with_no_alarmeringen(self):
        """
        If no alarmeringen exist, an empty list should be returned
        """
        response = self.client.get('/alarmeringen/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

        
class AlarmeringViewSetTests(APITestCase):
    fixtures = ['alarmeringen', 'regio', 'dienst']

    def test_index_view_with_alarmeringen(self):
        """
        If no alarmeringen exist, an empty list should be returned
        """
        response = self.client.get('/alarmeringen/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_index_view_with_subitems(self):
        """
        Alarmeringen should be displayed with their subitems
        """
        response = self.client.get('/alarmeringen/13156169/', format='json')
#        alarmering = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertEqual(len(alarmering['subitems']), 1)
#        self.assertEqual(alarmering['parent'], None)

    def test_index_view_with_no_subitems(self):
        """
        Alarmeringen with a parent should not return a result
        """
        response = self.client.get('/alarmeringen/13156191/', format='json')
#        alarmering = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertEqual(alarmering['parent'], '13156169')

    def test_datum(self):
        """
        Date fields should be formatted correctly
        """
        response = self.client.get('/alarmeringen/13156169/', format='json')
        s = json.loads(response.content)
        self.assertEqual(s['datum'], '2018-08-03')

    def test_capcodes(self):
        """
        Cap codes should be listed correctly
        """
        response = self.client.get('/alarmeringen/13156169/', format='json')
        s = json.loads(response.content)
        self.assertEqual(len(s['capcodes']), 3)
