FROM ubuntu:20.04

#Install base utilities for conda
RUN apt-get update && \
    apt-get install -y build-essential  && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ADD . /code
WORKDIR /code

COPY requirements requirements

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda create -n pysatell python=3.8.12
RUN conda init bash
#RUN conda activate pysatell
RUN conda install -n pysatell --file requirements
#RUN pip install -r requirements


