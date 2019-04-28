FROM python:3.6.6
LABEL maintainer="joe.jasinski@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true
ENV TERM linux

RUN apt-get update && apt-get install -y build-essential \
    git \
    apt-utils \
    software-properties-common \
    libjpeg-dev \
    libfreetype6 \
    libfreetype6-dev \
    zlib1g-dev \
    python3-dev \
    python3-venv \
    libpq-dev postgresql-client && rm -rf /var/lib/apt/lists/*


RUN groupadd -r app && \
    useradd -r -g app -d /home/app -s /sbin/nologin -c "Docker image user" app


ENV SITE_DIR=/site/
ENV NUM_THREADS=2
ENV NUM_PROCS=2
ENV DJANGO_DATABASE_URL=postgres://postgres@db/postgres

RUN install -g app -o app -d ${SITE_DIR}

WORKDIR ${SITE_DIR}
RUN install -g app -o app -d proj/ var/log/ htdocs/ htdocs/static/
RUN find /site/ -type d -exec chmod g+s {} \;
RUN chmod -R g+w /site/

RUN pip install pip --upgrade
RUN pip install uwsgi

COPY docker-utils/ssl/ ssl/
COPY requirements.txt requirements.txt
COPY requirements-test.txt requirements-test.txt
RUN pip install -r requirements-test.txt
COPY docker-utils/ docker-utils/
USER app

COPY . proj/

EXPOSE 8000
CMD ["./docker-utils/app-start.sh"]
ENTRYPOINT ["./docker-utils/entrypoint.sh"]

