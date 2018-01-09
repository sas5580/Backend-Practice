FROM ubuntu:latest
MAINTAINER Saswata Gupta "gupta.saswata@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["gunicorn", "-b 0.0.0.0:5000", "-w 2", "-k gevent", "run:app"]
