FROM python:3.9-slim

RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "/app/docker_entrypoint.py"]
