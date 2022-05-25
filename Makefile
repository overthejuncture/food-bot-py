init:
	docker run --workdir="/home" --user $$(id -u):$$(id -g) -v $$PWD/project:/home python:3.9.13 bash -c "python3 -m venv venv && . venv/bin/activate && python3 -m pip install -r requirements.txt"

run:
	docker-compose up -d

stop:
	docker-compose down
