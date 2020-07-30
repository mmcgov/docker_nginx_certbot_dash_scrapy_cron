FROM python:3.8-slim-buster
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update --fix-missing
RUN apt-get install -y \
        systemd \
        cron \
        vim \
        gcc \
        libffi-dev \
        libxml2-dev \
        libxslt-dev \
        musl-dev \
        python3-dev \
        python3-pip \
        curl ca-certificates \
    && update-ca-certificates

COPY ./ /home/scraper/
WORKDIR /home/scraper

RUN pip3 install -r ./requirements/base_requirements.txt

RUN chmod 755 ./scripts/entrypoint.sh 
RUN chmod 755 ./scripts/run.sh
COPY ./scripts/cron_scheduler /etc/cron.d/cron_scheduler
RUN chmod 755 /etc/cron.d/cron_scheduler
RUN crontab /etc/cron.d/cron_scheduler
RUN service cron start

ENTRYPOINT ["./scripts/entrypoint.sh"]

