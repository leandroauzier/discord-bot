FROM python:3.8.10

ARG DISCORD_TOKEN
ARG BEARER_PUBLIC_API
ARG HOST
ARG USER
ARG PASSWORD
ARG DATABASE

ENV DISCORD_TOKEN $DISCORD_TOKEN
ENV BEARER_PUBLIC_API $BEARER_PUBLIC_API
ENV HOST $HOST
ENV USER $USER
ENV PASSWORD $PASSWORD
ENV DATABASE $DATABASE

WORKDIR /app

RUN apt -y update && apt -y install libvips

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 discord_bot.py

CMD [ "python3", "-m", "http.server", "8080"]