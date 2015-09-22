# url_short_service
This repo contains the following files:
url_short.py -- python file to start cherrypy REST service to map full URLs to short URLs
Dockerfile -- dockerfile to setup url short service as a Docker app
Dockerrun.aws.json -- JSON file for launching the service as an Amazon Elastic Beanstalk


To run:
 
1. Build Docker image:
docker build -t urlshortservice .

2. Run Docker image:
docker run -p 32777:8080 urlshortservice

3. Connect to url shortening service:
http://<host url>:32777/api/UrlShortService


