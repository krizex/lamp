FROM centos:7.6.1810
ARG persist

RUN yum install -y epel-release
RUN yum install -y python-pip
RUN yum groupinstall -y "Development Tools"
RUN yum install -y python-devel

RUN yum install -y python-pip wget

# install ta-lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar xzvf ta-lib-0.4.0-src.tar.gz && cd ta-lib && ./configure --prefix=/usr && make && make install


COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

ENV LD_LIBRARY_PATH /usr/lib

COPY src/ /app/
COPY ${persist} /persist/
WORKDIR /app
EXPOSE 8000

CMD ./server.sh start
