FROM python:3

ADD fbot.py /
ADD botpackage /botpackage

RUN pip install requests websocket-client beautifulsoup4 pyparsing parsedatetime

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
