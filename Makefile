venv:
	docker run --volume ~/py/:/home --workdir="/home" python python3 -m venv venv

install-telebot:
	docker run --volume $$PWD:/home --workdir="/home" python python3 -m pip install telebot
