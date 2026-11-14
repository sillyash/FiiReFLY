from urllib.parse import urlsplit

from authlib.integrations.base_client import OAuthError
from django.conf import settings
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .arise import arise, display_name, user_from_userinfo

NEXT_SESSION_KEY = 'arise_next'
# login lancé depuis /admin/login/ -> on y retourne apres
ADMIN_SESSION_KEY = 'arise_admin'


def frontend_redirect(path='/'):
    """Redirect to a frontend route (the frontend uses hash routing)."""
    return HttpResponseRedirect(f'{settings.FRONTEND_URL}#{path}')


def safe_next(value):
    # Only plain frontend paths, never another host.
    if value and value.startswith('/') and not value.startswith('//'):
        return value
    return '/'


@require_GET
def login_view(request):
    # le callback arrive sur l'host de REDIRECT_URI : si on est sur un autre (127.0.0.1 vs
    # localhost), le cookie de session est pas le meme -> state oauth + flag admin perdus
    callback = urlsplit(settings.ARISE['REDIRECT_URI'])
    if request.get_host() != callback.netloc:
        return HttpResponseRedirect(
            f'{callback.scheme}://{callback.netloc}{request.get_full_path()}'
        )
    request.session[NEXT_SESSION_KEY] = safe_next(request.GET.get('next'))
    request.session[ADMIN_SESSION_KEY] = request.GET.get('admin') == '1'
    return arise.authorize_redirect(request, settings.ARISE['REDIRECT_URI'])


@require_GET
def callback_view(request):
    next_path = request.session.pop(NEXT_SESSION_KEY, '/')
    to_admin = request.session.pop(ADMIN_SESSION_KEY, False)
    try:
        token = arise.authorize_access_token(request)
        info = arise.userinfo(token=token)
    except OAuthError:
        return HttpResponseRedirect(reverse('admin:login')) if to_admin else frontend_redirect()
    login(request, user_from_userinfo(info))
    if to_admin:
        # si pas staff l'admin re-affiche le login avec un msg, c ok
        return HttpResponseRedirect(reverse('admin:index'))
    return frontend_redirect(next_path)


@require_POST
def logout_view(request):
    logout(request)
    return HttpResponse(status=204)


@require_GET
def me_view(request):
    user = request.user
    data = None
    if user.is_authenticated:
        data = {'id': user.pk, 'username': user.get_username(), 'name': display_name(user)}
    return JsonResponse({'user': data, 'csrfToken': get_token(request)})
