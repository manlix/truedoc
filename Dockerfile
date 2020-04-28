# Tags at Docker hub: https://hub.docker.com/_/python
FROM python:3.8.2-alpine3.11

# Place "truedoc" python package to this path on local filesystem
ARG TRUEDOC_PATH="/var/lib/truedoc"

RUN apk add uwsgi uwsgi-python3
COPY ./uwsgi/truedoc.ini /etc/uwsgi/

RUN mkdir -p ${TRUEDOC_PATH}
WORKDIR ${TRUEDOC_PATH}

# Copy required files to ${WORKDIR}
COPY ./requirements.txt .
COPY ./setup.py .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r ${TRUEDOC_PATH}/requirements.txt && \
    python3 setup.py develop

CMD /usr/sbin/uwsgi --ini /etc/uwsgi/truedoc.ini


# Docs about "Dockerfile": https://docs.docker.com/engine/reference/builder/
