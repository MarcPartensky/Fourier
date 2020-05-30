FROM python:3.8.3
ADD . /Fourier
WORKDIR /Fourier
RUN pip install -r requirements.txt
CMD ["python", "myfouriervf.py"]