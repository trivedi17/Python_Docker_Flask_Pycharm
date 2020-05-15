FROM python:3.8

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt --upgrade
RUN pip install flask-mysql

COPY . /app

CMD python app.py