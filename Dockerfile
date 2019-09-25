FROM python:3.7

ENV PYTHONUNBUFFERED 1
RUN mkdir /config
COPY requirements.txt /config
RUN mkdir /config
ADD /requirements /config/
ADD alembic.ini /
ADD .env /
RUN pip3 install --upgrade pip
RUN pip3 install -r /config/requirements.txt
RUN mkdir /src;
WORKDIR /src