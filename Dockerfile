FROM python:3.9-slim

LABEL maintainer="AXOLOTLTECH <s@saobby.com>"
LABEL description="SaobbyCAPTCHA-V3"
LABEL version="1.0"

RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
VOLUME ["./backgrounds", "./fonts", "./log"]
EXPOSE 5000
ENTRYPOINT ["python3", "/app/docker_entrypoint.py"]
