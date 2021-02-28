FROM python:3.8
WORKDIR /Blog
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/Blog \
    # DJANGO_SETTINGS_MODULE=config.settings.production \
    PORT=8000 \
    WEB_CONCURRENCY=3

EXPOSE ${PORT}

RUN pip install "gunicorn>=19.8,<19.9"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py runserver "0.0.0.0:${PORT}"

# RUN python manage.py collectstatic --noinput --clear

# CMD gunicorn config.wsgi:application