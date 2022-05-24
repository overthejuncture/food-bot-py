FROM python

RUN python3 -m venv /home/venv

RUN . /home/venv/bin/activate && python3 -m pip install pyTelegramBotAPI

COPY main.py /home/main.py

CMD . /home/venv/bin/activate && exec python main.py
