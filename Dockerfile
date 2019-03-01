# Name: bt.advform
# Author: Kenson Man <kenson@breakthrough.org.hk>
# Desc:   The file used to create the docker container that provide the advform application.
FROM django:1.9-python3
MAINTAINER Kenson Man <kenson@breakthrough.org.hk>

ADD dev/requirements.txt /usr/src/app/

RUN echo "Installating the system dependencies..." && \
  apt-get update && apt-get install -y postgresql libpq-dev python-dev     && \
  echo "Installating the django dependencies..."   && \
  pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app
EXPOSE 8000
CMD python /usr/src/app/manage.py runserver 0.0.0.0:8000
