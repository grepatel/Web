FROM python:3
WORKDIR /usr/local/app
ADD requirement.txt /usr/local/app
RUN pip3 install -r requirement.txt
ADD . /usr/local/app
