FROM python:3.10-slim-bullseye as build-common

RUN adduser --disabled-password --home /tiny --gecos '' tiny \
    && pip3 install --no-cache-dir --upgrade pip==22.0.4 pip-tools==6.6.0 \
    && mkdir /tiny/src && mkdir -p /build/python-base/

WORKDIR /build/
# Used to compute the path of the user site-packages directory when running pip install --user
ENV PYTHONUSERBASE "/build/python-base"
ENV PYTHONPATH "${PYTHONUSERBASE}/lib/python3.10/site-packages/"
ENV PATH "${PATH}:${PYTHONUSERBASE}/bin"

# common depedencies used in production and development
COPY requirements/base.txt requirements/base.txt
RUN pip-sync requirements/base.txt --pip-args '--no-cache-dir --no-deps --user'

ENV PYTHONPATH "/tiny/src"

### this stage is producing development artifacts and code-style checking and testing tools
FROM build-common as depedencies-development

RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/*

# depedencies used in development
COPY requirements/dev.txt requirements/dev.txt
RUN pip-sync requirements/base.txt requirements/dev.txt --pip-args '--no-cache-dir --no-deps --user'


### this stage is used to run the application in production and staging environments
FROM build-common as run-production
WORKDIR /tiny/src
USER tiny

COPY deployment/docker/run.sh /
COPY tiny tiny/
COPY alembic alembic/

ARG RELEASE
ENV RELEASE ${RELEASE}

# Group related env variables together to not create an independent docker layer for each of them
ENV FASTAPI_APP_FACTORY="tiny.__main__:create_app" FASTAPI_APP_HOST="0.0.0.0" FASTAPI_APP_RUN_PORT=8095

EXPOSE 8095

CMD ["/run.sh"]


### development stage should be as close as possible to production + extra development artifacts
FROM run-production as run-development
COPY --from=depedencies-development /usr/bin/git /usr/bin/git
COPY --from=depedencies-development /usr/lib/ /usr/lib/
COPY --from=depedencies-development /build/ /build/
