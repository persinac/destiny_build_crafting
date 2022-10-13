FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
RUN apt update
RUN apt-get install vim -y
RUN apt-get install lsof -y
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000", "--log-config", "log.ini"]