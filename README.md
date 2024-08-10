# Inventory Management System

A simple inventory management system for a cyberpunk-themed game
using FastAPI, SQLAlchemy, and PostgresSQL. The system manages items that players can
acquire in the game. These items could range from cybernetic enhancements to weapons and
gadgets. The API provides basic CRUD (Create, Read, Update, Delete) functionality for these
items.

## Table of contents

- [About project](#about-this-project)
    - [Motivation](#motivation)
    - [Conceptual decisions](#conceptual-decisions)
    - [Project structure](#project-structure)
    - [Project documentation](#project-documentation)
        - [Prerequisites](docs/PREREQUISITES.md)
        - [Project build and run](docs/README.md)
        - [API documentation](docs/api/README.md)
        - [Users documentation](docs/users/README.md)
    - [Technology stack](#technology-stack)

## About this project

### Motivation

While I've worked primarily with synchronous approaches in the past, this project allows me to apply and refine my
skills in working with asynchronous things.

### Conceptual decisions

#### Database schema

Decided to separate the `category` field into its own table and added a foreign key reference to the `Item` table,
allowing items to optionally be associated with a category with allowing the `Item` to exist without an associated
`Category`. `Item` and `Category` have references to each other by `sqlalchemy.orm.relationship`.

#### API module structure

Inventory CRUD functionality is placed in the `inventory` module separated by entity type.
Users CRUD is located in a separate module from inventory, as it does not directly relate to inventory functionality.
Due to separation pydentic `Item` and `Category` schemas they have cyclic references and that problem was resolved with
`__future__.annotations`, imports in the bottom and `schema.rebuild_model()`.

### API endpoints usage

Just for fun authorized active users without superuser privileges may have access to `items` related endpoints only.
Superusers have access to any `categories` and `items` endpoints.

### Project structure

```
├── docker                 | Dockerfiles and entrypointscripts 
├── migrations             | contains migrations separated in folders by DB name
│   └── postgresql
│       └── versions
├── src                    | contains project code
│   ├── api                | web API main module 
│   │   ├── inventory      | stuff related to CRUD functionality (endpoints, requests schemas, etc.)
│   │   │   ├── category
│   │   │   ├── item
│   │   ├── users          | users CRUD and auth part
│   │   └── utils          | utils include common stuff, dependencies, helpers, etc.
│   ├── db                 | module with DB's models, engines, sessions getters, etc.
│   │   ├── postgresql
└── tests
    ├── test_api
    │   ├── test_category
    │   └── test_item
    └── test_db

```

### Project documentation

- [Prerequisites](docs/PREREQUISITES.md)
- [Project build and run](docs/README.md)
- [API documentation](docs/api/README.md)
- [Users documentation](docs/users/README.md)

### Technology stack

- FastAPI
    - fastapi-users
    - pydantic
    - uvicorn
    - etc.
- DBs
    - PostgresSQL
        - asyncpg
        - sqlalchemy[asyncio]
        - etc.
    - Redis
    - Migrations
        - alembic
- Project dependencies
    - poetry
- Tests
    - pytest
    - pytest-asyncio
    - pytest-mock
    - pytest-cov
    - etc.
- Docker
    - docker compose v2
