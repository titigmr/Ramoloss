ARG ARCH

FROM arm32v7/python:3.7-buster as arch_armv7l
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
WORKDIR /ramoloss
COPY . .
RUN apt-get update && apt-get install libatlas-base-dev -y \
    && pip install --no-cache-dir -r requirements.txt \
    -i https://www.piwheels.org/simple


FROM python:3.7-buster as x86_64
ENV DISCORD_TOKEN=${DISCORD_TOKEN}
WORKDIR /ramoloss
COPY . .
RUN apt-get update && pip install --no-cache-dir \
    -r requirements.txt


FROM $ARCH
CMD [ "python", "main.py"]