# Tags at Docker hub: https://hub.docker.com/_/python
FROM python:3.7.4-alpine3.10

# Place "truedoc" python package to this path on local filesystem
ARG TRUEDOC_PATH="/var/lib/truedoc"

# ATTENTION: "FLASK_ENV=development" is required to automatic reload changed source code without rebuild containers.
# Docs: https://flask.palletsprojects.com/en/1.1.x/quickstart/#debug-mode
ENV FLASK_APP="truedoc.website:app" \
    FLASK_ENV="development"

RUN mkdir -p ${TRUEDOC_PATH}
WORKDIR ${TRUEDOC_PATH}

# Copy "requirements.txt" to ${WORKDIR}
COPY ./requirements.txt .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r ${TRUEDOC_PATH}/requirements.txt


EXPOSE 5000
CMD python -m flask run --host 0.0.0.0 --port 5000

# Docs about "Dockerfile": https://docs.docker.com/engine/reference/builder/
