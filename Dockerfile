FROM python:3.7.7-alpine

COPY . .
WORKDIR .

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python", "myfouriervf.py"]
