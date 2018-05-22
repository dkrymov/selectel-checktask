FROM python:2.7

WORKDIR /app
ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8000

ENV NAME My very first dock

RUN groupadd uwsgi && useradd -g uwsgi uwsgi
RUN chown -R uwsgi:uwsgi /app

CMD uwsgi --ini uwsgi.ini
