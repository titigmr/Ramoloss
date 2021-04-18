FROM python:3.8-slim-buster
WORKDIR /ramoloss
COPY . .
RUN pip install -r requirements.txt
CMD [ "python", "main.py"]
