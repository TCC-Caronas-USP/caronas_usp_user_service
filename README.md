# caronas_usp_user_service

## Scope

- Django 4.0.x
- Pre-commit hook
- Pipenv setup

## Container Installation

- `./dev_container_setup.bat`

## Manual/Local Installation

- `cd backend/`
- `pipenv install --dev`
- `pipenv run pre-commit install`

### Commands executed inside each container automatically

- `pipenv run python manage.py migrate`
- `pipenv run python manage.py runserver`

### Docker

1. Duplicate the `.env.sample` file and rename it to `.env`, if you haven't done it yet.

2. To start the container, run:

```
cd backend
docker-compose --profile=dev up --build -d
```

3. Create superuser

```
docker exec -it tcc_user_service pipenv run python manage.py createsuperuser
```

4. Point to http://localhost:8551

5. To stop and remove the containers, run:

```
docker-compose --profile=dev down
```

Para visualizar os logs do docker por um terminal separado (como o terminal do VSCode):

```
docker logs tcc_user_service -f
```

### Docker - debug

To run your application in docker in debug mode, follow the steps:

1. Duplicate the `.env.sample` file and rename it to `.env`, if you haven't done it yet.

2. To start the container, run:

```
cd backend
docker-compose --profile=debug up --build -d
```

3. Create superuser

```
docker exec -it tcc_user_service_debug pipenv run python manage.py createsuperuser
```

4. In VSCode's `Run and Debug` tab, choose the configuration `Python: Remote Attach` and press `Start Debugging`

5. Point to http://localhost:8551

6. To stop and remove the containers, run:

```
docker-compose --profile=debug down
```

### Linting and formatting

Linting is done by `flake8` and formatting by `black` and `isort`. They're configured to be performed on save and commit.

To perform a linter check and auto-formatting before after commit, use `pre-commit`:

```bash
$ pipenv run pre-commit install
```

If you want to format the whole project, you can run:

```bash
$ make format
```

Or, if you want to format a single file:

```bash
$ pipenv run black <filepath>
```

## Features

### Rest framework

- Code in `riders/views.py`
- Usage example for [postman](postman/*.json)

## Adicionando o endpoint

Como estamos usando o `ModelViewSet` para criar endpoints, precisamos que todos os métodos usados sejam especificados no `urls.py` através do campo `actions`. No geral a biblioteca irá associar os métodos de forma automática, mas idealmente devemos deixar os métodos explícitos mesmo que sejam "óbvios" (ex: `actions = {'post': 'post'}`).

Exemplo:

```
 path('aircraft/<int:pk>',
         AircraftView.as_view(
               customer_service=CustomerService(),
               actions={
                    'get': 'retrieve',
                    'post': 'post',
                    'patch': 'patch',
                    'delete': 'delete'
               }),
         name='detail_or_delete_or_edit_aircraft'),
```
