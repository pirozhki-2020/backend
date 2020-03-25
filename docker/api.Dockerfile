ARG PYTHON_VERSION=3.7-slim


FROM python:${PYTHON_VERSION} as builder
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc git
RUN pip install -U pip setuptools wheel

WORKDIR /wheels
COPY requirements.txt /
RUN pip wheel -r /requirements.txt


FROM python:${PYTHON_VERSION}
ENV PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
RUN pip install -U pip
RUN pip install /wheels/* \
        && rm -rf /wheels \
        && rm -rf /root/.cache/pip/*

WORKDIR /code
COPY . .

EXPOSE 8000
ENV PYTHONPATH /code
CMD ["gunicorn", "-c", "docker/gunicorn.conf", "backend.application.wsgi:application"]
