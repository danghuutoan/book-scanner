FROM python:3

WORKDIR /usr/src/app
RUN apt update -y && apt install -y postgresql-client
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .