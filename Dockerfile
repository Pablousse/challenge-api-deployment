# syntax=docker/dockerfile:1

FROM python:3.8
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN mkdir /api
COPY /api /api
EXPOSE 80
WORKDIR /api
CMD ["python", "app.py"]