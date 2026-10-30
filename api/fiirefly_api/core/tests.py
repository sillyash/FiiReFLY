from datetime import timedelta

from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APITestCase

from .models import LivreDorEntry, Soiree


class SoireeApiTests(APITestCase):
    def test_list_ordered_by_date(self):
        now = timezone.now()
        Soiree.objects.create(titre='Après', date=now + timedelta(days=2), lieu='BDE')
        Soiree.objects.create(titre='Avant', date=now + timedelta(days=1), lieu='BDE')

        response = self.client.get('/api/soirees/')

        self.assertEqual(response.status_code, 200)
        titres = [s['titre'] for s in response.data['results']]
        self.assertEqual(titres, ['Avant', 'Après'])

    def test_anonymous_cannot_create(self):
        response = self.client.post(
            '/api/soirees/', {'titre': 'x', 'date': timezone.now(), 'lieu': 'x'}
        )
        self.assertEqual(response.status_code, 403)


class LivreDorApiTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_anonymous_post_is_hidden_by_default(self):
        response = self.client.post('/api/livre-dor/', {'nom': 'Ash', 'message': 'Votez !'})

        self.assertEqual(response.status_code, 201)
        entry = LivreDorEntry.objects.get()
        self.assertFalse(entry.is_visible)

    def test_is_visible_cannot_be_set_by_client(self):
        self.client.post('/api/livre-dor/', {'nom': 'Ash', 'message': 'x', 'is_visible': True})
        self.assertFalse(LivreDorEntry.objects.get().is_visible)

    def test_list_is_not_exposed(self):
        response = self.client.get('/api/livre-dor/')
        self.assertEqual(response.status_code, 405)
