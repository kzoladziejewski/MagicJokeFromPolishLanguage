FROM python:3.11

RUN mkdir -p /backend_mpjfl

ADD . / backend_mpjfl/
WORKDIR backend_mpjfl
RUN pip install --upgrade pip
RUN python setup.py install
RUN python -m pip install -r requirements.txt
EXPOSE 8080

CMD ["python", "src/app.py"]