ARG BASE_IMAGE=python:3.9-slim-buster
FROM $BASE_IMAGE

WORKDIR .

# system update & package install
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    openssl libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# pip & requirements
COPY ./requirements.txt ./requirements.txt
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY . .


# Execute
CMD ["python", "main.py"]