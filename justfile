# FiiReFLY dev commands. Run `just` to list them.

[private]
default:
    @just --list --unsorted

# --- setup ---

# install everything
setup: web-setup api-setup hooks

# install web deps
web-setup:
    cd web && npm install

# install api deps + run migrations
api-setup:
    cd api && uv sync
    cd api && uv run manage.py migrate

# install pre-commit
hooks:
    uv tool install pre-commit
    pre-commit install

# --- dev ---

# run api + web
dev:
    #!/usr/bin/env bash
    trap 'kill 0' EXIT
    just api & just web & wait

# vite dev server
web:
    cd web && npm run dev

# Django dev server
api:
    cd api && uv run manage.py runserver

# create + apply migrations
migrate:
    cd api && uv run manage.py makemigrations
    cd api && uv run manage.py migrate

# create an admin login
superuser:
    cd api && uv run manage.py createsuperuser

# --- quality ---

# lint web + api
lint:
    cd web && npm run lint
    cd api && uv run ruff check --fix

# format web + api
fmt:
    cd web && npm run format
    cd api && uv run ruff format

# run every pre-commit
check:
    pre-commit run --all-files

# --- build ---

build:
    cd web && npm run build

preview: build
    cd web && npm run preview

# --- release ---

version:
    @echo "web $(cd web && npm pkg get version | tr -d '\"')  api $(cd api && uv version --short --color never)"

# bump web + api version
bump part="patch":
    #!/usr/bin/env bash
    set -euo pipefail
    test "$(git branch --show-current)" = main || { echo "bump from main only" >&2; exit 1; }
    test -z "$(git status --porcelain)" || { echo "working tree not clean" >&2; exit 1; }
    v=$(cd api && uv version --bump {{ part }} --short --color never)
    (cd web && npm version "$v" --no-git-tag-version --allow-same-version >/dev/null)
    git add api/pyproject.toml api/uv.lock web/package.json web/package-lock.json
    git commit -m "chore: bump version to $v"
    git tag "v$v"
    echo "bumped to v$v, run 'just deploy' to publish"

# push main + tag
deploy:
    #!/usr/bin/env bash
    set -euo pipefail
    test "$(git branch --show-current)" = main || { echo "deploy from main only" >&2; exit 1; }
    tag=$(git describe --tags --exact-match HEAD 2>/dev/null) || { echo "HEAD has no tag, run 'just bump' first" >&2; exit 1; }
    git push origin main
    git push origin "$tag"

clean:
    rm -rf web/dist
    find api -name __pycache__ -type d -exec rm -rf {} +
