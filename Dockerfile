ARG arch

FROM python:3.7-buster as x86_64
WORKDIR /ramoloss
COPY . .
RUN apt-get update && pip install --no-cache-dir \
    -r requirements.txt


FROM arm32v7/python:3.7-buster as armv7l
WORKDIR /ramoloss
COPY . .
RUN apt-get update && apt-get install libatlas-base-dev -y \
    && pip install --no-cache-dir -r requirements.txt \
    -i https://www.piwheels.org/simple


FROM ${arch}
CMD [ "python", "main.py"]
