FROM python:3.8-slim-buster
WORKDIR /ramoloss
COPY . .
RUN apt-get update \ 
    && apt-get install build-essential make gcc -y \
    && apt-get install dpkg-dev -y \ 
    && apt-get install libjpeg-dev -y \ 
    && pip install -r requirements.txt \
    && pip install --no-cache-dir . \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get auto-remove -y \
    && rm -rf /var/lib/apt/lists/* \
    && find /usr/local/lib/python3.7 -name "*.pyc" -type f -delete
CMD [ "python", "main.py"]
