ARG PYTHON_VERSION=3.7-slim

FROM python:${PYTHON_VERSION} as builder
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc git
RUN pip install -U pip setuptools wheel

WORKDIR /wheels
COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /code
COPY . .
RUN python manage.py collectstatic --noinput

FROM nginx:alpine
COPY --from=builder /code/static/ /usr/share/nginx/html/dj_static
EXPOSE 80 80
