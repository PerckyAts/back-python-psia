# syntax=docker/dockerfile
FROM archlinux:latest

RUN pacman -Syu               \
    --noconfirm              \
    make   python3 python-pip nano

WORKDIR /

COPY ./code /code

WORKDIR /code

RUN python3 -m venv env

RUN source env/bin/activate

RUN env/bin/pip install -r requirements.txt

ADD ./entrypoint.sh /entrypoint.sh
RUN chmod 755  /entrypoint.sh

EXPOSE 9000

ENTRYPOINT ["/entrypoint.sh"]