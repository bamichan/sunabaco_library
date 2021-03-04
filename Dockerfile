FROM nikolaik/python-nodejs:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /sunabaco_app
WORKDIR /sunabaco_app

COPY . /sunabaco_app
COPY ./nginx/gunicorn /var/run/gunicorn
COPY ./nginx /etc/nginx

RUN apt-get update && \
    apt-get install -y build-essential libzbar-dev
RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install pyzbar
RUN pip install -r requirements.txt

EXPOSE 8000

COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
CMD [ "node", "server.js" ]
ENTRYPOINT ["init.sh"]
