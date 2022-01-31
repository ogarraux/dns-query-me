FROM python:3.9.10-slim

RUN apt update
RUN apt install -y git
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN mkdir /app
COPY dns.py /app
WORKDIR /app
ENTRYPOINT ["./dns.py"]
EXPOSE 53/udp
EXPOSE 53/tcp
