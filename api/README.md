# API

Django REST Framework

## Dev

```bash
uv sync
cp .env.example .env  # puis remplir
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

- API : http://127.0.0.1:8000/api/
- Admin : http://127.0.0.1:8000/admin/

## Variables d'environnement

Lues depuis l'environnement ou `api/.env` (cf. [`.env.example`](.env.example)).

| Variable                        | Defaut                                                        | Role                          |
| ------------------------------- | ------------------------------------------------------------- | ----------------------------- |
| `FIIREFLY_DEBUG`                | `true`                                                        | `false` en prod               |
| `FIIREFLY_SECRET_KEY`           | cle locale si debug                                           | obligatoire en prod           |
| `FIIREFLY_ALLOWED_HOSTS`        | `localhost,127.0.0.1`                                         | domaines de l'API             |
| `FIIREFLY_CORS_ALLOWED_ORIGINS` | `http://localhost:5173`                                       | origines du front             |
| `FIIREFLY_CSRF_TRUSTED_ORIGINS` | origines CORS                                                 | origines HTTPS de confiance   |
| `FIIREFLY_DB_PATH`              | `db.sqlite3`                                                  | chemin de la DB SQLite        |
| `FIIREFLY_STATIC_ROOT`          | `staticfiles`                                                 | sortie de `collectstatic`     |
| `FIIREFLY_FRONTEND_URL`         | `http://localhost:5173/`                                      | URL du front (avec `/` final) |
| `FIIREFLY_ARISE_CLIENT_ID`      | vide                                                          | client Arise Connect          |
| `FIIREFLY_ARISE_CLIENT_SECRET`  | vide                                                          | secret du client              |
| `FIIREFLY_ARISE_ISSUER`         | `https://oidc.iiens.net`                                      | serveur OAuth Arise           |
| `FIIREFLY_ARISE_SCOPES`         | `openid profile user.profile user.id user.preferred_nickname` | scopes demandes               |
| `FIIREFLY_ARISE_REDIRECT_URI`   | `http://localhost:8000/auth/callback/`                        | callback OAuth                |

## Arise Connect

Login via OAuth (authorization code + PKCE), le code est echange cote API
(le serveur OAuth n'autorise pas le CORS).

1. Creer un client sur https://connect.iiens.net/dashboard/clients :
   - Token Endpoint Auth Method : `Client Secret Basic`
   - Grant type `authorization_code`, response type `code`
   - Redirect URI : `FIIREFLY_ARISE_REDIRECT_URI` (pas de `#` possible)
2. Renseigner `FIIREFLY_ARISE_CLIENT_ID` et `FIIREFLY_ARISE_CLIENT_SECRET` dans `api/.env`.

Routes :

| Route             | Role                                                   |
| ----------------- | ------------------------------------------------------ |
| `/auth/login/`    | redirige vers Arise, `?next=/route-du-front` au retour             |
| `/auth/callback/` | retour d'Arise, redirige au front sur `#/connexion?code=...`       |
| `/auth/token/`    | `POST {code}`, echange le code (valable 2 min) contre un token     |
| `/auth/logout/`   | `POST`, supprime le token                                          |
| `/auth/me/`       | utilisateur connecte (ou `null`)                                   |

## Production

Deploye sur le RasPi homelab a https://fiirefly-api.sillyash.com (Gunicorn + nginx,
via Cloudflare Tunnel). Config et scripts dans le repo homelab :
`services/fiirefly/` ([README](https://github.com/sillyash/homelab/tree/main/services/fiirefly)).

```bash
# remote = git@github.com:sillyash/FiiReFLY.git
git -C ~/FiiReFLY pull
sudo ~/homelab/services/fiirefly/deploy.sh
```

- API : https://fiirefly-api.sillyash.com/api/
- Admin : https://fiirefly-api.sillyash.com/admin/
