FROM python:3.11.3-slim

RUN pip install -U pip
RUN pip install pipenv 

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy


COPY [ "predict.py", "./" ]

COPY [ 'dict_vect.bin', 'model.pkl',"./" ]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]