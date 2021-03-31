FROM python:3.8-slim-buster

WORKDIR /simple-blc

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=developement

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
