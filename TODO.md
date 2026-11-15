# TODO

## Tooling

justfile
- [x] setup
- [x] web-setup
- [x] api-setup

pre-commit
- [x] api
  - [x] ruff lint + format
  - [x] uv lock
  - [x] django check + migrations
- [x] web
  - [x] lint + format + type-check
- [x] general
  - [x] bump version (`just bump`)
  - [x] deploy (push w/ tags) (`just deploy`)


## Web

### Squelette

- [ ] deps + filesystem
- [x] routing
- [x] page programme (statique)
- [x] page membres (trombi lucioles, click -> detail)
- [x] header
- [x] footer
- [x] css base
  - [x] theme
  - [x] footer/header/main spacing
  - [x] dark mode

## API


### Setup

- [x] settings
- [x] deps (REST Framework + CORS)
- [x] livre d'or (POST only)
- [x] dates de soirees (GET only)
- [x] admin dashboard
- [x] livre d'or GET (que les visibles)
- [x] trombi : poles (couleur) + membres, photo crop carré webp
- [x] role "Liste" sur l'admin + login admin via arise
- [ ] mapper un groupe arise -> role Liste (sinon a la main dans l'admin)

### Deploiement

- [x] gunicorn + settings prod (proxy HTTPS, `FIIREFLY_STATIC_ROOT`)
- [x] homelab : systemd + nginx + deploy.sh (`services/fiirefly/`)
- [ ] cert + route Cloudflare Tunnel `fiirefly-api.sillyash.com`
- [ ] redirect URI Arise Connect en prod
- [ ] nginx : `location /media/` -> `FIIREFLY_MEDIA_ROOT` (photos trombi)
