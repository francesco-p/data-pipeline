FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y exiftool
RUN apt-get install -y openjdk-8-jdk
RUN apt-get install -y python3-dev python3-pip

RUN pip install instaloader 
RUN pip install minio 
RUN pip install pyspark 
RUN pip install numpy
RUN pip install pandas
RUN export PYSPARK_SUBMIT_ARGS="--master local pyspark-shell"

RUN mkdir /code 
COPY ./app/src/ /code
WORKDIR /code
CMD ["python3", "main.py"]
