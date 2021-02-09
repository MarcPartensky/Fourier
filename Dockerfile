FROM python:3.8.3-alpine

COPY . .
WORKDIR .

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python", "myfouriervf.py"]
