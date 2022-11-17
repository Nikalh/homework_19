FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN  pip install -r requirements.txt
COPY app.py .
COPY config.py .
COPY setup_db.py .
ADD  views views
ADD  service service
ADD  dao dao
COPY constants.py .
COPY implemented.py .
COPY movies.db .
COPY migrations migrations
COPY docker_config.py default_config.py

CMD flask run -h 0.0.0.0 -p 80