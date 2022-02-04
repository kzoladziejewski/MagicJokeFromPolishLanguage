FROM python:3.9

RUN mkdir -p /backend_mpjfl

WORKDIR backend_mpjfl
COPY ../../../backend_mpjfl/ ./
RUN ls
RUN python setup.py install
RUN python -m pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "mpjfl/app.py"]