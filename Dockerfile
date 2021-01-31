FROM python:3.9

RUN pip install pipenv
WORKDIR /app
COPY Pipfile.lock .
RUN pipenv sync

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

CMD pipenv run flask run --host=0.0.0.0