# This is a comment

FROM ubuntu:14.04

MAINTAINER Jason Hartmann <hartmann4@msn.com> 

EXPOSE 8080

RUN apt-get install -y python 

RUN apt-get -y install curl 

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py

RUN pip install cherrypy

ADD  /url_short /url_short

CMD python /url_short/url_short.py
