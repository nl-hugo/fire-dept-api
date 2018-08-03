import json
from rest_framework import status
from django.test import TestCase
from datetime import datetime
from alarmeringen.models import Alarmering

from rest_framework.test import APITestCase


class AlarmeringModelTests(TestCase):
    fixtures = ['alarmeringen']

    def test_brandinfo(self):
        s = Alarmering.objects.get(pk='13156169')
        self.assertEqual(s.brandinfo, 'buitenbrand')

    def test_datum(self):
        s = Alarmering.objects.get(pk='13156169')
        self.assertEqual(datetime.strftime(s.datum, '%Y-%m-%d'), '2018-08-03')

    def test_capcodes(self):
        s = Alarmering.objects.get(pk='13156169')
        self.assertEqual(s.capcodes.count(), 3)

    def test_parent(self):
        p = Alarmering.objects.get(pk='13156169')
        self.assertEqual(p.parent, None)

        c = Alarmering.objects.get(pk='13156191')
        self.assertEqual(c.parent, p)

    def test_subitems(self):
        p = Alarmering.objects.get(pk='13156169')
        self.assertEqual(p.subitems.count(), 1)

        c = Alarmering.objects.get(pk='13156191')
        self.assertEqual(c.subitems.count(), 0)


class AlarmeringEmptyViewSetTests(APITestCase):

    def test_index_view_with_no_alarmeringen(self):
        """
        If no alarmeringen exist, an empty list should be returned
        """
        response = self.client.get('/alarmeringen/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])


class AlarmeringViewSetTests(APITestCase):
    fixtures = ['alarmeringen']

    def test_index_view_with_alarmeringen(self):
        """
        If no alarmeringen exist, an empty list should be returned
        """
        response = self.client.get('/alarmeringen/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_index_view_with_subitems(self):
        """
        Alarmeringen should be displayed with their subitems
        """
        response = self.client.get('/alarmeringen/13156169/', format='json')
        alarmering = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(alarmering['subitems']), 1)

    def test_index_view_with_no_subitems(self):
        """
        Alarmeringen with a parent should not return a result
        """
        response = self.client.get('/alarmeringen/13156191/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
