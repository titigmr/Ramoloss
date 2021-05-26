FROM python:3.7-stretch
WORKDIR /ramoloss
COPY . .
RUN apt-get update \ 
    && apt-get install build-essential make gcc -y \
    && apt-get install dpkg-dev -y \ 
    && apt-get install libjpeg-dev -y \ 
    && pip install --upgrade pip \
    && pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple \
    && apt install python3-numpy

CMD [ "python", "main.py"]
