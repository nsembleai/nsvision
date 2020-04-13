FROM python:3.6-slim

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y \
&& apt-get install -y --no-install-recommends apt-utils \
&& apt-get install -y libglib2.0-0 \
&& apt install -y libsm6 \
&& apt-get install -y libxrender1 \
&& apt-get install -y libxext6

RUN pip install --upgrade pip \
&& pip install opencv-python \
&& pip install nsvision