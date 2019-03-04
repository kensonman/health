FROM python:3-alpine

LABEL maintainer="Kenson Man <kenson@kenson.idv.hk>"
LABEL version=v1.0.0

ENV WDIR=/usr/src/app

COPY src/ ${WDIR}/


RUN echo ">>   Installing dependancies..." \
 && mkdir -p /var/log/supervisor \
 && apk update \
 && apk upgrade \
 && apk add --update --no-cache bash gettext build-base postgresql-dev jpeg-dev nginx supervisor zlib-dev uwsgi-python3 vim linux-headers \
 && adduser -S thisuser \
 && mkdir -p /scripts \
 && mkdir -p ${WDIR}/logs \
 && mkdir -p /usr/share/nginx/html/.well-know \
 && mkdir -p /var/log/uwsgi \
 && chown -R thisuser:www-data /var/log/uwsgi \
 && echo ">>   Finishing ..."

COPY scripts/*  /scripts/

RUN echo ">>   Configurating ..." \
 && chown -R thisuser:www-data /usr/src/app \
 && chmod +x /scripts/entrypoint \
 && pip install uwsgi \
 && pip install -r ${WDIR}/requirements.txt \
 && ${WDIR}/manage.py collectstatic --no-input \
 && chown -R thisuser:www-data ${WDIR} \
 && ln -s /scripts/entrypoint /usr/bin/entrypoint \
 && sed -i "s/__PYTHONPATH__/.`python -c \"import os,sys;print(os.pathsep.join(sys.path).replace('/', '\/'))\"`/g" /scripts/supervisord.conf \
 && echo ">>   Finishing..."

EXPOSE 80

ENTRYPOINT ["/scripts/entrypoint"]
CMD ["run"]
WORKDIR ${WDIR}
