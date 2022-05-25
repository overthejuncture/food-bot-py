FROM python:3.9.13

COPY requirements.txt /home

#RUN python3 -m venv /home/venv

#RUN . /home/venv/bin/activate && python3 -m pip install -r requirements.txt

WORKDIR /home

CMD . /home/venv/bin/activate && exec python main.py
