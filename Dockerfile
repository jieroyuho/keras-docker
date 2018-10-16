FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
#RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \ 
        curl \
        python3 \ 
        python3-dev \
        python3-setuptools \  
	git 


RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

RUN pip3  --no-cache-dir install \
        tensorflow==1.7.1 \
        pandas \
        sklearn \
        scipy \
        keras==2.1.5 \
        matplotlib \
        numpy==1.14.5 \
        h5py \ 
        jupyter \
        ipykernel \
        && \
    python3 -m ipykernel.kernelspec

RUN apt-get install -y --no-install-recommends\
    vim \
    mariadb-server \
    mariadb-client 

WORKDIR "root"

COPY VGG16_5485_For5.h5 /root

#VOLUME ["/works"]

#CMD ["/bin/bash"]
ENTRYPOINT service mysql restart && bash