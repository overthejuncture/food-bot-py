setvenv:
	docker build --tag py:venv -f Dockerfile.venv .
	docker run -v $$PWD/venv:/home/venv py:venv

after:
	docker build --tag py .
	docker run -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py --network check-network --network-alias python py

runnod:
	docker run -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py --network check-network --network-alias python py

run:
	docker run -d -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py --network check-network --network-alias python py

bash:
	docker run -it -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py --network check-network --network-alias python py bash

bashold:
	docker run -it -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py py bash

mysql:
	docker run -d --env-file .env -p 3306:3306 --name mysql --network check-network --network-alias mysql mysql:5.7

mysqlold:
	docker run -d --env-file .env -p 3306:3306 --name mysql mysql:5.7

create_network:
	docker network create check-network

inspect_network:
	docker network inspect bridge
