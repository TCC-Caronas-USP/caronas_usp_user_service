echo off
cls
echo Fazendo setup do container de dev...
echo.
echo VERIFIQUE EM QUAL PYTHON O PIPENV SERA INSTALADO!
echo.
echo Sera utilizado:
py --version
echo.
echo Se este Python nao for o correto, aperte Cntrl+C para sair
pause
cd backend
py -m pip install pipenv
pipenv install --dev
pipenv run pre-commit install
copy .env.sample .env
docker-compose --profile=dev up --build -d
echo.
echo Crie seu superuser:
echo.
docker exec -it tcc_user_service pipenv run python manage.py createsuperuser
