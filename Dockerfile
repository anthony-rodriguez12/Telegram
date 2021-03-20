FROM python:3.9

RUN pip install --upgrade pip\
    && mkdir \app

ADD . /app

WORKDIR /app

RUN pip install -r requeriments.txt

CMD python /app/bot.py 

