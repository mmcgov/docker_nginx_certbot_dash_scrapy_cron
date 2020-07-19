FROM mmg/scraper

RUN apt-get update --fix-missing
RUN apt-get install -y \
        systemd \
        cron \
        vim \
        gcc \
        nginx

WORKDIR /home/dash_app
COPY ./ ./
RUN pip3 install -r ./requirements/base_requirements.txt

EXPOSE 80
RUN chmod 755 ./scripts/entrypoint.sh
ENTRYPOINT ["./scripts/entrypoint.sh"]

