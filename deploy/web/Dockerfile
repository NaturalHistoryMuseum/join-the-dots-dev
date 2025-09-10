FROM node:latest

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  mariadb-client

COPY ./deploy/web/entrypoint /entrypoint
COPY ./ /app

WORKDIR /app

RUN npm i

ENTRYPOINT ["/bin/bash", "/entrypoint"]

CMD npm run dev -- --host 0.0.0.0
