FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install neofetch -y
COPY . /app
RUN pip3 install -r requirements.txt
CMD bash start.sh