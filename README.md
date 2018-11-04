# django_coins

Test Project


## Prerequisites

You will need:

- `python3.6` (see `Pipfile` for full version)
- `postgresql` with version `10`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Documentation

Full documentation is available here: [`docs/`](docs).


## Run tests

`docker-compose -f docker-compose.yml -f docker-compose.test.override.yml up --build`


## Dev server

- `docker-compose -f docker-compose.yml -f docker-compose.dev.override.yml up --build`
- API can be accessed via [http://127.0.0.1:8001/v1/]()
- Swaggger [http://127.0.0.1:8001/v1/]()
