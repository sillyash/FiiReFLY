from urllib.parse import quote, urlsplit

from authlib.integrations.base_client import OAuthError
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.core import signing
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_GET
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .arise import arise, display_name, user_from_userinfo

NEXT_SESSION_KEY = 'arise_next'
# login lancé depuis /admin/login/ -> on y retourne apres
ADMIN_SESSION_KEY = 'arise_admin'

# code court passe au front apres le login, echange contre un token par /auth/token/
LOGIN_CODE_SALT = 'fiirefly.accounts.login-code'
LOGIN_CODE_MAX_AGE = 120


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
    # le front est sur un autre site : pas de cookie, il recupere un token avec ce code
    code = signing.dumps(request.user.pk, salt=LOGIN_CODE_SALT)
    return frontend_redirect(f'/connexion?code={code}&next={quote(next_path)}')


def user_payload(user):
    return {'id': user.pk, 'username': user.get_username(), 'name': display_name(user)}


@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def token_view(request):
    try:
        pk = signing.loads(
            str(request.data.get('code', '')), salt=LOGIN_CODE_SALT, max_age=LOGIN_CODE_MAX_AGE
        )
        user = get_user_model().objects.get(pk=pk, is_active=True)
    except (signing.BadSignature, get_user_model().DoesNotExist):
        return Response({'detail': 'Code invalide ou expire.'}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': user_payload(user)})


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    # un seul token par user : ca deconnecte tous ses appareils
    Token.objects.filter(user=request.user).delete()
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def me_view(request):
    user = request.user
    return Response({'user': user_payload(user) if user.is_authenticated else None})
