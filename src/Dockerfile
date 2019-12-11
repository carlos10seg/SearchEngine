FROM ubuntu:18.04

RUN apt update && \
    apt install -y python3.6 && \
    apt install -y python3-pip && \
    apt install -y mongodb

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN mkdir /data
RUN mkdir /data/db

COPY . /app

EXPOSE 5000

CMD ["python3", "app.py"]