FROM python:3.8-slim AS bot

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PIP_DEFAULT_TIMEOUT=100



RUN apt-get update
RUN apt-get -y install -qq --force-yes python3 python3-pip  build-essential
RUN mkdir /var/app
COPY divar.py /var/app/divar.py
COPY main.py /var/app/main.py
COPY requirements.txt /var/app/requirements.txt
RUN pip install -r /var/app/requirements.txt


CMD ["python", "/var/app/main.py"]
