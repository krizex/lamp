FROM centos:7.6.1810

RUN yum install -y epel-release
RUN yum install -y python-pip

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt


COPY src/ /app/
COPY _build/datatmp/ /db/
WORKDIR /app

CMD ./server.sh start
