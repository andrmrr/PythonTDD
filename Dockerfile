FROM python:3.13-slim

RUN apt-get update
RUN apt-get install -y logwatch
RUN echo "/usr/sbin/logwatch --output mail --mailto andrejaandrejic00@gmail.com --detail high" >> /etc/cron.daily/00logwatch
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src

WORKDIR /src

RUN python manage.py collectstatic

ENV DJANGO_DEBUG_FALSE=1
CMD gunicorn --bind :8888 superlists.wsgi:application

# RUN addgroup --system nonroot && adduser --system --no-create-home --disabled-password --group nonroot

# USER nonroot