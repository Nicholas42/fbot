FROM python:3
COPY entrypoint.sh /
ADD fbot.py /
ADD botpackage /botpackage
RUN pip install requests websocket-client
ENTRYPOINT ["/entrypoint.sh"]
