FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
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
#COPY VGG16_5485_Label.py /root
#COPY VGG16Run.sh /root
#COPY datafilter.py /root
#COPY makedatasetunknown.py /root
#COPY post_freqarray.py /root
#COPY post_freqarray_combine.py /root
#COPY freqrun.sh /root
#COPY freq.sql /root
#RUN service mysql restart
#RUN sh ./freqrun.sha


#VOLUME ["/works"]
#CMD ["/bin/bash"]

#ENTRYPOINT service mysql restart && bash
ENTRYPOINT cp VGG16_5485_For5.h5 /data/ && cd /data && sh freqrun.sh > /data/freq.log 2>&1 && bash
