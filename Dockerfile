# syntax=docker/dockerfile:1

FROM python:3.8
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /app
COPY . /app
EXPOSE 80
CMD ["python", "app/app.py"]