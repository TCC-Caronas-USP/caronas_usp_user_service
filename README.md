# caronas_usp_user_service


## Container Installation

- `./dev_container_setup.bat`

### Comandos úteis

#### Para abrir um terminal dentro do container:
- `docker exec -it tcc_user_service bash`

#### Para criar as migrações:
- `docker exec -it tcc_user_service pipenv run python manage.py makemigrations`
(se estiver usando o terminal dentro do container, n precisa colocar o `docker exec -it tcc_user_service` no começo)

#### Para reverter as migrações:
- `docker exec -it tcc_user_service pipenv run python manage.py migrate riders zero`
(se estiver usando o terminal dentro do container, n precisa colocar o `docker exec -it tcc_user_service` no começo)


#### Para rodar o container:

```
cd backend
docker-compose --profile=dev up --build -d
```

#### Para criar um superuser (admin):

```
docker exec -it tcc_user_service pipenv run python manage.py createsuperuser
```

Acessar http://localhost:8551/admin e logar com as credenciais configuradas no comando acima

#### Para desinstalar o container:

```
docker-compose --profile=dev down
```

#### Para visualizar os logs do docker por um terminal separado (como o terminal do VSCode):

```
docker logs tcc_user_service -f
```

#### Para rodar o container em modo debug:


```
cd backend
docker-compose --profile=debug up --build -d
```

#### Para criar um superuser (admin):

```
docker exec -it tcc_user_service_debug pipenv run python manage.py createsuperuser
```

#### Na aba do VSCode `Run and Debug`, escolher configuração `Python: Remote Attach` e clicar `Start Debugging`

Acessar http://localhost:8551

#### Para desinstalar o container:

```
docker-compose --profile=debug down
```
