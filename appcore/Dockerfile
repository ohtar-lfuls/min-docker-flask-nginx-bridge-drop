FROM python:3.13

WORKDIR /AppCore

COPY requirements.txt /AppCore/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uwsgi","--ini","uwsgi.ini"]