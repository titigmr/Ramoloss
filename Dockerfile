FROM python:3.7-stretch
WORKDIR /ramoloss
COPY . .
RUN apt-get update \ 
    && apt-get install build-essential \ 
    tk-dev libncurses5-dev libncursesw5-dev \
    libreadline6-dev libdb5.3-dev libgdbm-dev \
    libsqlite3-dev libssl-dev libbz2-dev \
    libexpat1-dev liblzma-dev \
    zlib1g-dev libffi-dev libatlas-base-dev -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple \
    && pip uninstall numpy -y \
    && apt install python3-numpy -y
CMD [ "python", "main.py"]
