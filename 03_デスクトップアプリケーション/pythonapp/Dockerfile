# https://hub.docker.com/r/continuumio/anaconda3
FROM continuumio/anaconda3:2019.03

# RUN pip install [packages]

WORKDIR /workdir

COPY app.py /workdir

ENTRYPOINT ["python", "app.py"]
