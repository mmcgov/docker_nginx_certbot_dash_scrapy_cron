build:
	docker-compose build --pull

stack-up:
	docker-compose up -d

stack-purge:
	docker-compose stop
	docker-compose kill
	docker-compose rm

stack-full-refresh:
	docker-compose build --no-cache --pull

build-scraper:
	docker-compose build scraper --pull

build-dash-app:
	docker-compose build dash_app

run-scraper:
	docker-compose run --rm scraper python3 /home/scraper/scripts/scraper/scraper/spiders/scraper.py 

run-dash-app-dev:
	docker-compose run --rm -p 80:80 dash_app python3 /home/dash_app/scripts/dash_site.py

run-dash-app-full:
	docker-compose run --rm --publish 80:80 dash_app gunicorn -b 0.0.0.0:80 wsgi:app

bash-scraper:
	docker-compose run --rm --entrypoint "/bin/bash -c" scraper bash 

bash-dash-app:
	docker-compose -f docker-compose.yaml run --rm --entrypoint "/bin/bash -c" dash_app bash

bash-nginx:
	docker-compose -f docker-compose.yaml run --rm --entrypoint "/bin/sh -c" nginx sh

bash-certbot:
	docker-compose -f docker-compose.yaml run --rm --entrypoint "/bin/sh -c" certbot sh

launch-on-local:
	docker-compose -f docker-compose-local.yaml up 

launch-on-server:
	docker-compose -f docker-compose.yaml up 
