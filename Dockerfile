#FROM python:3.7-stretch
FROM debian:stretch-slim
WORKDIR /ramoloss
COPY . .
RUN apt-get update && apt-get -y dist-upgrade \
    && apt-get -y install build-essential make libssl-dev \
    libffi-dev python3.5 libblas3 libc6 liblapack3 \
    gcc python3-dev python-pip cython3 python3-numpy \
    && pip install --upgrade pip setuptools wheel cmake \
    && pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple 
CMD [ "python", "main.py"]
