FROM alpine:3.10.2

# Install some system utilities for Python to use
RUN apk update && apk upgrade && apk add gcc musl-dev libc-dev libc6-compat linux-headers build-base libffi-dev openssl-dev

# Install Node, Make, Python and Git
RUN apk add --update make git bash python3 python3-dev
COPY pip-reqs.txt /
RUN cat pip-reqs.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r /pip-reqs.txt
