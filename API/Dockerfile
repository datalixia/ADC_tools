FROM python:3.9

WORKDIR /code

RUN apt-get update && apt-get install -y cmake libboost-all-dev

COPY ./code/requirements.txt /code/requirements.txt

RUN pip install --default-timeout=100 --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./code /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888","--reload"]