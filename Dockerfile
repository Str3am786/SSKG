### 1. Get Linux
FROM alpine:3.7

### 2. Get Java via the package manager
RUN apk update \
&& apk upgrade \
&& apk add --no-cache bash \
&& apk add --no-cache --virtual=build-dependencies unzip \
&& apk add --no-cache curl \
&& apk add --no-cache openjdk8-jre \
&& apk add python3 python3-dev gcc g++ gfortran musl-dev libxml2-dev libxslt-dev

ENV JAVA_HOME=/opt/java/openjdk \
    PATH="/opt/java/openjdk/bin:$PATH"


RUN pip3 install --upgrade pip requests
RUN pip3 install python-docx wheel tika numpy
RUN pip3 install pandas
