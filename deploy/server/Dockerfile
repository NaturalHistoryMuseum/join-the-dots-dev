FROM python:latest

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  python3-dev \
  mariadb-client

COPY ./deploy/server/entrypoint /entrypoint
COPY ./ /app

WORKDIR /app

RUN pip install -e .

ENTRYPOINT ["/bin/bash", "/entrypoint"]

CMD flask run --host 0.0.0.0 --port 8000
