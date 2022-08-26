FROM python:3.9-buster
    
ENV DEBIAN_FRONTEND=noninteractive
 
RUN apt-get update && apt-get install -y \
		libx11-dev \
		python-tk

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN echo 'alias awsume=". awsume"' >> /root/.bashrc

COPY pyproject.toml poetry.lock ./
RUN poetry install
