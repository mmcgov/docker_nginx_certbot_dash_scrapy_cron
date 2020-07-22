# docker-compose nginx certbot dash scrapy<br>

## Quick start guide:
1) Git clone this repo
2) Move the env file to `.env`
3) change the email and domain variables in this `.env` file to your personal values
4) Update email and domain details in init-letsencrypt.sh script and run. I discovered this script at the below site and included it in this template as it gets round the problem of needing nginx to perform the Let’s Encrypt validation But nginx won’t start if the certificates are missing. The script creates a dummy certificate, start nginx, delete the dummy and request the real certificates
https://medium.com/@pentacent/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71
5) Finally `docker-compose up` and your website should be fully up and running with ssl encryption and a scheduled refresh of data collected from a scrapy job. Note the certbot container automatically checks at regualr intervals if certificates need renewal as well so no need to manually renew when certificates expire in 90 days.

### NOTE:
If using copy of this repo locally ensure below files are removed so as to avoid conflicts with certificates etc.
1) Run `rm -r certbot/*` this will clean out the certbot docker and when you docker compose up it will take from files from the official certbot image for your specific site.
2) Also the app.conf file in the nginx folder should be cleaned and elft empty to be repopulated by the template file when you docker compose up. It should overwrite but just in case best to clean out the app.conf file and leave it as an empty file.

## Summary
This docker-compose project is designed to streamline the process of building a multicontainer project where for example a scraper is collecting data at regular intervals whcih is then being visualized on a dash/flask website with full ssl encryption.

The way I designed this project you only need to change the domain name and email address variables essentially to get the docker running for your specific domain.

The docker-compose runs 4 services (scraper, dash_app, certbot and nginx):

### Scraper
Scrapy is a python library for web scraping at scale. It is asynchronous and can scrape large quantities at speed.

This service is built from scratch using a lightweight python base image (`python:3.8-slim-buster`). It installs all the requirements needed for scrapy.
The service itself is a scrapy job to collect data from a specific site. The code will need to be tailored for that site in terms of scraping logic etc. The example script is scraping some covid19 statistics from worldometers website.
This scraper is designed to run as a cron job at any desired frequency. To change the frequency simply change the schedule inside the scheduler script saved at scraper/scripts/scraper_scheduler.sh. This command in this file is added at build time inside the dockerfile and then the command cron -f runs when the build is finished running the cron in the foreground. This final command is in the docker-compose file and is necessary for the cron schedule to run successfully.

### dash_app
Dash is a python library from plotly that builds upon plotly basic functionality to develop interactive analytics that can be served on a website without having to learn html etc.

This service launches a dash app based on the data from the scraper. Once again this docker is built rather than using an image. It builds on top of the scraper image to save rebuilding the python base image. For this reason I used the `depends_on` command to ensure it waits until the scraper docker is built before it starts to build.
It launches the dash_app via gunicorn web server to make it more robust than a pure flask dev server.
`gunicorn --workers 3 -b 0.0.0.0:8000 wsgi:app`

Note we expose port `8000:8000` here from docker to host so we can just run the dash_app for local testing with no need to run nginx/certbot. 

We also connect this to the internal network we name docker_network which links this to the nginx docker.

### certbot
Certbot is used to generate the ssl certificate using letsencrypt. This ensures the site we launch is secure. 

This service takes the official docker image for certbot and uses it directly with no modifications so no dockerfile is required to make custom build like the scraper and dash_app services is necessary. Two volumes are shared with the certbot which are initially empty in the docker. So essentially we are copying the data in these volumes from the docker to the outside folder. Then we share this outside folder with Nginx later and in this way we easily share the folders from the certbot docker to the nginx docker.

Also note I pass environment variables into this docker including email and domain name. These come from the `.env` file stored in same directory as the yaml file. Any variables in `.env` file are available in the docker-compose yaml file. However if you want to use them inside the docker they need to be passed in from the yaml file (see the nginx docker for example), you cant just use variables from the .env file directly inside the docker. 
Finally the entrypoint checks if certificates need renewed and sets up a regular checkup to make sure they are renewed when appropriate.

### nginx
nginx is a reverse proxy for your site and helps manage incoming traffic or can simple help serve static files.

This service takes the official docker image of nginx similar to the certbot service so no dockerfile is necessary. We then pass in the environment variables from `.env` and the volumes created by the certbot service. 

We map two ports from the docker to the out side:
`80:80` this is the default port for a website meaning if you just enter the domain name with no port number it will and here which is what we want to save having to append a port number to the end of our site url.
`443:443` this is the default port for ssl requests so we want to collect all those requests to connect them with our ssl certificate.

We also connect this to the internal network we name docker_network which links this to the dash_app docker.

There is only two files inserted into this docker, app.conf and app.conf.template. We use the `envsubst` command to push the variables from the yaml file into the app.conf.template file inside the docker and save it as app.conf. The nginx service then picks this conf file up and uses it to run the nginx service for your specific domain. Note inside the conf file the first server block pushes all requests to ssl requests and the second server block links to the upstream dash_app on port 8000 which gunicorn is running on. This second server block then displays the output from the dash_app coming from port 8000 on the website domain.

## Docker-compose yaml files
1) docker-compose.yaml - Runs full service hosting data on chosen domain.
2) docker-compose-local.yaml - Runs scraper and dash_app on localhost:8000 for dev and local testing.






