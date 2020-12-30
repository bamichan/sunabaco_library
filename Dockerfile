FROM nikolaik/python-nodejs:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /sunabaco_app
WORKDIR /sunabaco_app

COPY . /sunabaco_app
COPY ./nginx/gunicorn /var/run/gunicorn
COPY ./nginx /etc/nginx

RUN apt-get update && apt-get install -y \
    pkg-config \
    libgtk2.0-dev \
    libzbar0 \
    libopencv-dev \
    libv4l-dev \
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r requirements.txt

EXPOSE 8000

COPY init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh
CMD [ "node", "server.js" ]
ENTRYPOINT ["init.sh"]