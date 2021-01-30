FROM python:alpine

ADD ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

RUN mkdir app
WORKDIR /app
RUN mkdir blog
COPY run.py run.py

ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD python run.py

