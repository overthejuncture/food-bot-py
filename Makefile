setvenv:
	docker build --tag py:venv -f Dockerfile.venv .
	docker run -v $$PWD/venv:/home/venv py:venv

after:
	docker build --tag py .
	docker run -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py py

runnod:
	docker run -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py py

run:
	docker run -d -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py py

bash:
	docker run -it -v $$PWD/venv:/home/venv -v $$PWD/main.py:/home/main.py py bash

