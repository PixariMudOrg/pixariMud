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

dev-setup:
	uv run pre-commit install

lint:
	uv run ruff check --fix pixarimud/
	uv run ruff format pixarimud/

# TODO: Add docker installation for the on-server setup so it's easy and consistent with a make setup && make deploy
