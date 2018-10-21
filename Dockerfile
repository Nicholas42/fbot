FROM python:3
ADD fbot.py settings.py /
ADD botpackage /botpackage
RUN pip install requests websocket-client
CMD ["python", "-u", "./fbot.py"]
