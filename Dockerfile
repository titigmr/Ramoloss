FROM python:3.7-buster
WORKDIR /ramoloss
COPY . .
RUN apt-get update && pip install --no-cache-dir \
    -r requirements.txt
CMD [ "python", "main.py"]
