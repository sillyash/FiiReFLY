# API

Django REST Framework

## Dev

```bash
uv sync
uv run manage.py migrate
uv run manage.py createsuperuser
uv run manage.py runserver
```

- API : http://127.0.0.1:8000/api/
- Admin : http://127.0.0.1:8000/admin/

## Variables d'environnement

| Variable                        | Defaut                  | Role                      |
| ------------------------------- | ----------------------- | ------------------------- |
| `FIIREFLY_DEBUG`                | `true`                  | `false` en prod           |
| `FIIREFLY_SECRET_KEY`           | cle locale si debug     | obligatoire en prod       |
| `FIIREFLY_ALLOWED_HOSTS`        | `localhost,127.0.0.1`   | domaines de l'API         |
| `FIIREFLY_CORS_ALLOWED_ORIGINS` | `http://localhost:5173` | origines du front         |
| `FIIREFLY_CSRF_TRUSTED_ORIGINS` | vide                    | origines HTTPS de l'admin |
| `FIIREFLY_DB_PATH`              | `db.sqlite3`            | chemin de la DB SQLite    |
