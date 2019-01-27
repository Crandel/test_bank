FROM python:3-alpine

WORKDIR /opt/code

COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps && \
    pip install --no-cache-dir -U pip && \
    pip install -r requirements.txt && \
    find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + && \
    runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

COPY . .


EXPOSE 8000

CMD [ "python", "./manage.py runserver 0.0.0.0:8000" ]
