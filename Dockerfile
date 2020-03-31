FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV IS_CONTAINERIZED 1
RUN mkdir /config
ADD /config/requirements.txt /config/
RUN pip install -r /config/requirements.txt
RUN mkdir /code
WORKDIR /code
COPY . .
