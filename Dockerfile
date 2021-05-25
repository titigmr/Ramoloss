FROM python:3.8-slim-buster
WORKDIR /ramoloss
COPY . .
RUN pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple
CMD [ "python", "main.py"]
