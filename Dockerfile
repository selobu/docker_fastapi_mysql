# sistema operativo y el servidor proxy http
FROM ubuntu/nginx:edge

# etiquetas del proyecto
LABEL "com.example.vendor"="SL SERVICIOS LATAM SAS"
LABEL "version"="1.0"
LABEL "description"="TEST FLASKAPI"
LABEL "autor"="Sebastian López Buriticá"
LABEL "email"='selobu@gmail.com'

RUN apt update
RUN apt upgrade -y

# base de datos sql mariadb
# https://mariadb.org/download/?t=repo-config&d=22.04+%22jammy%22&v=10.6&r_m=uni_frontera
RUN apt-get install apt-transport-https curl -y
RUN curl -o /etc/apt/trusted.gpg.d/mariadb_release_signing_key.asc 'https://mariadb.org/mariadb_release_signing_key.asc'
RUN sh -c "echo 'deb https://mirror.ufro.cl/mariadb/repo/10.6/ubuntu jammy main' >>/etc/apt/sources.list"
RUN apt-get update
RUN apt-get install mariadb-server -y

# python y pip
RUN apt install -y python3.10
RUN apt install -y python3-pip

# instalando el servidor wsgi
RUN pip install gunicorn --no-cache-dir

# instalando dependencias de python
RUN pip install flask==2.2.2 sqlalchemy==1.4.41 flask-sqlalchemy==2.5.1 flask_cors==3.0.10 \
        flask_restx==0.5.1 alembic==1.5.4 flask_migrate jinja2 fpdf2 pyjwt==2.1.0 \
        flask-jwt-extended==4.4.0 pygments flask-WTF flask-bootstrap \
        flask-login flask_admin flask_uploads flask_script docutils pygal xlrd \
        pymysql --no-cache-dir

# directorio de trabajo
WORKDIR /app
COPY package*.json ./

# allow to execute server config
RUN chmod +x /start.sh

# Exponer puertos
# EXPOSE 80
CMD ["sh"]
# docker build -t selobu:flasktest .