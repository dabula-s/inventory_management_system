## Project build and run

## Table of contents

- [ENV files](#env-files)
- [Run services](#run-services)
- [Apply migrations](#apply-migrations)
- [Run tests](#run-tests)

### ENV files

Copy `.env.example`, `.env.test.example` and `.env.test.local.example` into files without `.example` postfix:

```bash
cp .env.example .env
cp .env.test.example .env.test
cp .env.local.example .env.local
```

### Run services

1. To run dev version with `--reload` option:

```bash
docker compose -f docker-compose-dev.yaml up --build
```

or

```bash
docker compose -f docker-compose-dev.yaml build
docker compose -f docker-compose-dev.yaml up
```

2. To run project without dev dependencies installed and without `--reload` option:

```bash
docker compose up --build
```

or

```bash
docker compose build
docker compose up
```

### Apply migrations

Usually migration are applied on every start of `api` service. But you can apply/generate migrations manually:

```bash
alembic -n postgresql upgrade head
```

```bash
alembic -n postgresql revision --autogenerate -m "some message"
```

### Run tests

You can run migrations locally in terminal or inside the container.

> **WARNING**
>
> Tests could be run only in dev `api-service` that was built from `Dockerfile.dev`
> because it includes installation of dev project dependencies.

1. In terminal:

```bash
ENVIRONMENT=local pytest tests/
```

2. In `app` container:

```bash
docker exec api-service ENVIRONMENT=docker pytest tests/
```