from unittest import mock

from django.http import HttpResponseRedirect
from django.test import TestCase, override_settings

from . import views

ARISE = {**views.settings.ARISE, 'REDIRECT_URI': 'http://localhost:8000/auth/callback/'}


@override_settings(ARISE=ARISE, ALLOWED_HOSTS=['localhost', '127.0.0.1'])
class AriseLoginTests(TestCase):
    def test_bounce_vers_host_du_callback(self):
        response = self.client.get('/auth/login/?admin=1', HTTP_HOST='127.0.0.1:8000')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://localhost:8000/auth/login/?admin=1')

    def test_login_admin_revient_sur_admin(self):
        host = {'HTTP_HOST': 'localhost:8000'}
        redirect = HttpResponseRedirect('https://oidc.example/auth')
        with mock.patch.object(views.arise, 'authorize_redirect', return_value=redirect):
            self.client.get('/auth/login/?admin=1', **host)

        with (
            mock.patch.object(views.arise, 'authorize_access_token', return_value={}),
            mock.patch.object(views.arise, 'userinfo', return_value={'id': 'dupontj2042'}),
        ):
            response = self.client.get('/auth/callback/', **host)

        self.assertEqual(response['Location'], '/admin/')
