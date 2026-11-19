import shutil
import tempfile
from datetime import timedelta
from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone
from PIL import Image
from rest_framework.test import APITestCase

from fiirefly_api.accounts.models import Profile

from .models import LivreDorEntry, Membre, Pole, Soiree
from .roles import LISTE_GROUP, LISTE_PERMISSIONS

User = get_user_model()
MEDIA_TMP = tempfile.mkdtemp()


def fake_photo(w=800, h=400, name='photo.png'):
    buf = BytesIO()
    Image.new('RGB', (w, h), 'pink').save(buf, 'PNG')
    return SimpleUploadedFile(name, buf.getvalue(), content_type='image/png')


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
        self.assertEqual(response.status_code, 401)


class LivreDorApiTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user('dupontj2042')
        Profile.objects.create(user=self.user, nickname='Ash')

    def test_anonymous_cannot_post(self):
        response = self.client.post('/api/livre-dor/', {'message': 'Votez !'})
        self.assertEqual(response.status_code, 401)
        self.assertFalse(LivreDorEntry.objects.exists())

    def test_post_uses_arise_name(self):
        self.client.force_authenticate(self.user)
        response = self.client.post('/api/livre-dor/', {'message': 'Votez !'})

        self.assertEqual(response.status_code, 201)
        entry = LivreDorEntry.objects.get()
        self.assertEqual(entry.nom, 'Ash')
        self.assertEqual(entry.auteur, self.user)

    def test_client_cannot_set_nom_or_visibility(self):
        self.client.force_authenticate(self.user)
        self.client.post('/api/livre-dor/', {'nom': 'Fake', 'message': 'x', 'is_visible': False})

        entry = LivreDorEntry.objects.get()
        self.assertEqual(entry.nom, 'Ash')
        self.assertTrue(entry.is_visible)

    def test_list_only_visible_newest_first(self):
        LivreDorEntry.objects.create(nom='a', message='vieux')
        LivreDorEntry.objects.create(nom='b', message='cache', is_visible=False)
        LivreDorEntry.objects.create(nom='c', message='recent')

        response = self.client.get('/api/livre-dor/')

        self.assertEqual(response.status_code, 200)
        messages = [e['message'] for e in response.data['results']]
        self.assertEqual(messages, ['recent', 'vieux'])


@override_settings(MEDIA_ROOT=MEDIA_TMP)
class MembreTests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TMP, ignore_errors=True)

    def test_list_visible_with_poles_no_pagination(self):
        com = Pole.objects.create(nom='Com', couleur='#123456', ordre=2)
        bureau = Pole.objects.create(nom='Bureau', ordre=1)
        Membre.objects.create(nom='Zoe').poles.add(com)
        Membre.objects.create(nom='Alex', role='Prez').poles.add(bureau)
        Membre.objects.create(nom='Cache', is_visible=False)
        Membre.objects.create(nom='Sans pole')

        response = self.client.get('/api/membres/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual([m['nom'] for m in response.data], ['Alex', 'Zoe', 'Sans pole'])
        pole = {'id': com.id, 'nom': 'Com', 'couleur': '#123456', 'ordre': 2}
        self.assertEqual(response.data[1]['poles'], [pole])
        self.assertEqual(response.data[2]['poles'], [])

    def test_multi_poles_listed_once_sorted_by_main_pole(self):
        bureau = Pole.objects.create(nom='Bureau', ordre=1)
        asso = Pole.objects.create(nom='Asso', ordre=2)
        com = Pole.objects.create(nom='Com', ordre=3)
        Membre.objects.create(nom='Zoe').poles.add(asso)
        # pole principal = Bureau, donc avant Zoe
        Membre.objects.create(nom='Yann').poles.add(com, bureau)

        response = self.client.get('/api/membres/')

        self.assertEqual([m['nom'] for m in response.data], ['Yann', 'Zoe'])
        self.assertEqual([p['nom'] for p in response.data[0]['poles']], ['Bureau', 'Com'])

    def test_photo_cropped_square_webp(self):
        membre = Membre.objects.create(nom='Alex', photo=fake_photo())

        self.assertTrue(membre.photo.name.endswith('.webp'))
        with Image.open(membre.photo.path) as img:
            self.assertEqual(img.format, 'WEBP')
            self.assertEqual(img.size, (512, 512))

    def test_old_photo_deleted_on_change(self):
        membre = Membre.objects.create(nom='Alex', photo=fake_photo())
        old = membre.photo.name

        membre.photo = fake_photo(300, 900, 'autre.png')
        membre.save()

        self.assertNotEqual(membre.photo.name, old)
        self.assertFalse(membre.photo.storage.exists(old))
        self.assertTrue(membre.photo.storage.exists(membre.photo.name))

    def test_edit_without_new_photo_keeps_it(self):
        membre = Membre.objects.create(nom='Alex', photo=fake_photo())
        name = membre.photo.name

        membre.role = 'Prez'
        membre.save()

        self.assertEqual(membre.photo.name, name)
        self.assertTrue(membre.photo.storage.exists(name))


class ListeRoleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('membreliste', is_staff=True)
        self.user.groups.add(Group.objects.get(name=LISTE_GROUP))
        self.client.force_login(self.user)

    def test_group_has_exactly_liste_perms(self):
        group = Group.objects.get(name=LISTE_GROUP)
        perms = sorted(f'{p.content_type.app_label}.{p.codename}' for p in group.permissions.all())
        self.assertEqual(perms, LISTE_PERMISSIONS)

    def test_can_manage_content(self):
        for url in [
            '/admin/core/membre/',
            '/admin/core/pole/add/',
            '/admin/core/soiree/add/',
            '/admin/core/livredorentry/',
        ]:
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_cannot_touch_users_or_post_livre_dor(self):
        for url in ['/admin/auth/user/', '/admin/core/livredorentry/add/']:
            self.assertEqual(self.client.get(url).status_code, 403, url)
