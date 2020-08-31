FROM python:3.8
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
RUN pip install pipenv
RUN pipenv install --deploy --system
CMD exec gunicorn --bind :5000 --workers 1 --threads 8 app.main:app