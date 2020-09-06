FROM python:3.7

MAINTAINER chlv lvchongen@gmail.com

ADD queryMac.py /

RUN pip install requests

RUN pip install beautifulsoup4

ENTRYPOINT [ "python", "/queryMac.py"]