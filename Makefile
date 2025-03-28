build:
	docker-compose build

migrate:
	docker exec $(docker ps -q -f name=pixarimud_evennia) evennia migrate

deploy:
	docker stack deploy -c docker-compose.yml pixarimud

remove:
	docker stack rm pixarimud

setup:
	sudo apt-get update && sudo apt-get install -y \
		gcc \
		clang \
		pkg-config \
		default-libmysqlclient-dev \
		build-essential
