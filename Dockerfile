FROM python:3.9.4-slim

COPY . /opt
WORKDIR /opt

LABEL maintainer="marc.partensky@gmail.com"
LABEL source="https://github.com/marcpartensky/fourier"
RUN apt-get update
RUN apt-get install -y libx11-dev libgl-dev libgtk-3-dev

RUN pip install -U pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/opt/__main__.py"]
CMD ["python", "/opt/__main__.py"]
