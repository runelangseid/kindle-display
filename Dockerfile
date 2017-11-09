#FROM python:3
#
##EXPOSE 5000
#
#RUN mkdir /app
#COPY ./app /app
#WORKDIR /app
#
#COPY requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt
#
#ENTRYPOINT ["python"]
#CMD python kindle-flask.py
##CMD ['app/main.py']


FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
