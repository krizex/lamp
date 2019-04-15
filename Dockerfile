FROM centos:7.6.1810 as builder

RUN yum install -y epel-release
RUN yum groupinstall -y "Development Tools"
RUN yum install -y wget

# install ta-lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && tar xzvf ta-lib-0.4.0-src.tar.gz && cd ta-lib && mkdir /usr-tmp && ./configure --prefix=/usr-tmp && make && make install


FROM centos:7.6.1810
ARG persist

RUN yum install -y epel-release
RUN yum install -y python-pip wget
RUN yum groupinstall -y "Development Tools"
RUN yum install -y python-devel

# install ta-lib
COPY --from=builder /usr-tmp /usr
ENV LD_LIBRARY_PATH /usr/lib

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

COPY src/ /app/
COPY ${persist} /persist/
WORKDIR /app
EXPOSE 8000

CMD ./server.sh start
