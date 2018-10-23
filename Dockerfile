FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
#RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \ 
        curl \
        python3 \ 
        python3-dev \
        python3-setuptools \  
	git \
        vim \ 
        mariadb-server \ 
        mariadb-client 



RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

RUN pip  --no-cache-dir install \
        tensorflow==1.11.0 \
        pandas \
        sklearn \
        scipy \
        keras \
        matplotlib \
        numpy \
        h5py \ 
        jupyter \
        ipykernel \
        pymysql
    
WORKDIR "root"

COPY VGG16_5485_For5.h5 /root
COPY freqrun.sh /root
COPY freq.sql /root
#VOLUME ["/works"]

#CMD ["/bin/bash"]
#ENTRYPOINT service mysql restart && bash
ENTRYPOINT service mysql restart && sh ./freqrun.sh && bash
#CMD ["/freqrun.sh", "--alow-root"]
