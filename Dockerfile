FROM python:3.7.7-alpine

COPY . /opt

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python", "/opt/__main__.py"]
