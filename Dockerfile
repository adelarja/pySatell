FROM python:3.8-bullseye
WORKDIR /code
COPY requirements requirements
RUN pip install -r requirements


