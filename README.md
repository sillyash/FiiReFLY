# FiiReFLY

## Stack

- VueJS : frontend
  - Deploy sur les pages perso de l'ecole : https://fiirefly.iiens.net
- Django : API + DB
  - Deploy sur le RasPi homelab @sillyash : https://fiirefly-api.sillyash.com

### Prerequis

- NodeJS
- Python
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- [`just`](https://github.com/casey/just)

## Structure

- [`api/`](api/) - Django backend
- [`web/`](web/) - VueJS frontend

`README` respectifs dans chaque sous-projet.

## Features

> [!TIP]
>
> Voir GitHub Issues !

## Dev

> [!TIP]
> Installer [`just`](https://github.com/casey/just) pour
> utiliser les commandes (cf. [justfile](justfile)) rapides !

### Setup

Avoir installe les prerequis ([ici](#prerequis)) !

```bash
just setup
```

> eh ouais c simple pas vrai ?

Installe les dependances NodeJS et Python.

Pour voir les autres commandes:

```bash
just
```

### Organisation

Si possible:
- S'organiser avec GitHub issues
- Faire des branches -- `main` seulement pour les merge car trigger les deploy
- Mettre a jour les issues
- Kiffer
- Eviter au plus possible les LLM -- exceptions possibles pour debug -- on est la pour creer !
