FROM docker-local.artifactory.cloud2.athenahealth.com/athenahealth-base-centos7:0.0.6

RUN yum update -y && yum install python-pip -y

RUN pip install prometheus_client && pip install requests

RUN mkdir /opt/kafkascraper

WORKDIR /opt/kafkascraper

COPY ./init.sh ./

COPY ./find_kafka_stats.py ./

ENTRYPOINT [ "/bin/bash", "init.sh"]