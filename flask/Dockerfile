FROM python:alpine

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN mkdir app
WORKDIR /app
RUN mkdir flask_blog

ENV FLASK_APP=flask_blog
ENV FLASK_ENV=development

CMD flask run --host=0.0.0.0

