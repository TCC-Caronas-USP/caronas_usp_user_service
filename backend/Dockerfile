FROM python:3.9.6

WORKDIR /code
COPY . /code/
COPY Pipfile* ./
RUN pip install pipenv && pipenv install
EXPOSE 8000
