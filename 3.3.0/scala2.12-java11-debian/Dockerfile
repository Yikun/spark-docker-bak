#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
FROM debian:bullseye-slim

ARG spark_uid=185

# Before building the docker image, first build and make a Spark distribution following
# the instructions in https://spark.apache.org/docs/latest/building-spark.html.
# If this docker file is being used in the context of building your images from a Spark
# distribution, the docker build command should be invoked from the top level directory
# of the Spark distribution. E.g.:
# docker build -t spark:latest -f kubernetes/dockerfiles/spark/Dockerfile .

RUN set -ex && \
    apt-get update && \
    ln -s /lib /lib64 && \
    apt install -y wget bash tini libc6 libpam-modules krb5-user libnss3 procps openjdk-11-jre net-tools && \
    mkdir -p /opt/spark && \
    mkdir -p /opt/spark/examples && \
    mkdir -p /opt/spark/work-dir && \
    touch /opt/spark/RELEASE && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    chgrp root /etc/passwd && chmod ug+rw /etc/passwd && \
    rm -rf /var/cache/apt/*

# TODO: GPG validation
ARG DISTRO_NAME=spark-3.3.0-bin-hadoop3
ARG SHORT_DISTRO_NAME=spark-3.3.0
RUN wget https://dlcdn.apache.org/spark/$SHORT_DISTRO_NAME/$DISTRO_NAME.tgz
RUN tar zxvf $DISTRO_NAME.tgz

WORKDIR $DISTRO_NAME

RUN mv jars /opt/spark/
RUN mv bin /opt/spark/
RUN mv sbin /opt/spark/
# RUN mv kubernetes/dockerfiles/spark/entrypoint.sh /opt/
COPY entrypoint.sh /opt/
RUN mv kubernetes/dockerfiles/spark/decom.sh /opt/
RUN mv examples /opt/spark/
RUN mv kubernetes/tests /opt/spark/
RUN mv data /opt/spark/

RUN rm -rf $DISTRO_NAME $DISTRO_NAME.tgz

ENV SPARK_HOME /opt/spark

WORKDIR /opt/spark/work-dir
RUN chmod g+w /opt/spark/work-dir
RUN chmod a+x /opt/decom.sh
RUN chmod a+x /opt/entrypoint.sh

ENTRYPOINT [ "/opt/entrypoint.sh" ]

# Specify the User that the actual main process will run as
USER ${spark_uid}