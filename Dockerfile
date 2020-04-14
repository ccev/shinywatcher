FROM python:3.7-slim

WORKDIR /app
COPY . /app

RUN pip install requests pymysql
RUN chmod +x run.sh

ENTRYPOINT ["./run.sh"]