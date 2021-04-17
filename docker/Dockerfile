FROM ubuntu:18.04

ARG python=3.6
ENV PYTHON_VERSION=${python}

## accelerate debugging by building most-static layers first 
## install libraries first 
RUN apt-get update && apt-get install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
        build-essential \
        cmake \
        g++-4.8 \
        git \
        curl \
        vim \
        wget \
        ca-certificates \
        python3.6 \
        python3.6-dev \
	&& \
    apt-get install -y python3.6-distutils && \
    ln -s /usr/bin/python3.6 /usr/bin/python && \
    curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py && \
    mkdir -p /app

## second, add requirements 
ADD src/python/requirements.txt /app/requirements.txt 
RUN pip install -r /app/requirements.txt 

## finally, add code itself 
ADD src /app/src

WORKDIR "/app"
