FROM python:3.8

WORKDIR /schedule-bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080
EXPOSE 5432

CMD [ "python", "./main.py" ]