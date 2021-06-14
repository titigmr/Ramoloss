FROM arm32v7/python:3.7-buster
WORKDIR /ramoloss
COPY . .
RUN apt-get update && apt-get install libatlas-base-dev -y && pip install --no-cache-dir -r requirements.txt -i https://www.piwheels.org/simple
CMD [ "python", "main.py"]
