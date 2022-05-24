FROM python

RUN python3 -m venv /home/venv

RUN . /home/venv/bin/activate && python3 -m pip install pyTelegramBotAPI mysql-connector-python

#COPY main.py /home/main.py

WORKDIR /home

CMD . /home/venv/bin/activate && exec python main.py
