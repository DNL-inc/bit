FROM python:3.8-slim

WORKDIR /bit

COPY requirements.txt /bit/
RUN pip install -r /bit/requirements.txt
COPY . /bit/

CMD python3 /bit/app.py