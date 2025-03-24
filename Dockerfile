FROM evennia/evennia:latest

WORKDIR /usr/src/game/evennia
ENTRYPOINT ["evennia", "start", "-l"]
