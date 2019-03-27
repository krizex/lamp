FROM centos:7.6.1810
ARG persist

RUN yum install -y epel-release
RUN yum install -y python-pip

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

COPY src/ /app/
COPY ${persist} /persist/
WORKDIR /app
EXPOSE 8000

CMD ./server.sh start
