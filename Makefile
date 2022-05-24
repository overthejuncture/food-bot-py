venv:
	docker run --volume ~/py/:/home --workdir="/home" python python3 -m venv venv

install-telebot:
	docker run --volume $$PWD:/home --workdir="/home" python python3 -m pip install telebot

runnod:
	docker run -v $$PWD/main.py:/home/main.py py:main

run:
	docker run -d -v $$PWD/main.py:/home/main.py py:main

bash:
	docker run -it py:main bash
