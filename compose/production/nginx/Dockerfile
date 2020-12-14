FROM nginx:1.19.5-alpine

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY server.conf /etc/nginx/conf.d

RUN mkdir /data \
    && mkdir /data/nginx \
    && mkdir /data/nginx/temp \
    && mkdir /data/nginx/cache
EXPOSE 80
