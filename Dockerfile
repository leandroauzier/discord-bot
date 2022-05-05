FROM python:3.8.10

ENV DISCORD_TOKEN ${DISCORD_TOKEN}
ENV BEARER_PUBLIC_API ${BEARER_PUBLIC_API}
ENV HOST ${HOST}
ENV USER ${USER}
ENV PASSWORD ${PASSWORD}
ENV DATABASE ${DATABASE}

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "discord_bot.py"]