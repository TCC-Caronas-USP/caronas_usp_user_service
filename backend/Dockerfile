FROM python:3.9.6

WORKDIR /usr/src/app
COPY Pipfile* ./
RUN pip install pipenv && pipenv install
EXPOSE 8000
