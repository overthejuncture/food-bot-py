include .env
export

init:
	docker run --workdir="/home" --user $$(id -u):$$(id -g) -v $$PWD/project:/home python:3.9.13 bash -c "python3 -m venv venv && . venv/bin/activate && python3 -m pip install -r requirements.txt"
	make filldb

filldb:
	docker-compose up -d
	docker compose exec mysql mysqladmin -u root -p$(DB_PASSWORD) create food_bot_py
	docker compose down

run:
	docker-compose up -d

stop:
	docker-compose down
