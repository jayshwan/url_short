# This is a comment

FROM ubuntu:20.04

MAINTAINER Jason Hartmann <hartmann4@msn.com> 

EXPOSE 8080

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get -y install curl 

RUN apt-get -y install python3-pip

RUN pip3 install cherrypy

ADD /url_short /url_short

CMD python3 /url_short/url_short.py
