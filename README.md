# keras-docker

docker login 

docker build -t jiero/keras-docker:0.5 .

docler image ls

docker push jiero/keras-docker:0.5



# Docker run with ENV setting 

- In run.sh 

echo $ENV1
echo $ENV2


- In Dockerfile

ENTRYPOINT sh run.sh && /bin/bash  


- In Command 

docker run -it -e ENV1="HELLO" -e ENV2="World!" image  

docker run -it -v /fileDirection/:/data/  -e fName="filename.csv" image  

 
