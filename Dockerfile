FROM ubuntu

LABEL maintainer="onsoim <onsoim@gmail.com>" 

RUN apt-get update

RUN apt-get install -y \
	python3 \
	python3-pip \
	libmysqlclient-dev

RUN pip3 install \
	django \
	django-bootstrap4 \
	mysqlclient

WORKDIR /project

ENTRYPOINT \
	apt-get install -y mysql-server && \
	service mysql start && \
	mysql < settings.sql && \
	python3 manage.py migrate && \
	python3 manage.py runserver 0.0.0.0:8080

# docker build -t oss . && docker run --rm -it -p 80:8080 -v $(pwd)/project:/project oss
