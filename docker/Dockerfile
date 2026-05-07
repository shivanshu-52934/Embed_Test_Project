FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3 \
    python3-pip \
    gcovr \
    lcov

WORKDIR /app

COPY . /app

RUN pip3 install pytest

CMD ["bash"]