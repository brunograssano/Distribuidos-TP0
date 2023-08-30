FROM alpine:latest
RUN apk add --update --no-cache netcat-openbsd
COPY netcat/run_netcat.sh run_netcat.sh
ENTRYPOINT ["/bin/sh"]