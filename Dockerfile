FROM python:3.6-alpine

RUN apk add --update alpine-sdk glib glib-dev linux-headers

RUN mkdir /app

WORKDIR /app

COPY ./shoe_sensor/ /app/shoe_sensor/
COPY ./setup.py /app/setup.py
COPY ./README.md /app/README.md
COPY ./requirements.txt /app/requirements.txt

RUN pip install .

CMD ["python", "-m", "shoe_sensor.tools.collect_data_csv_local", "-m", "/app/macs.txt", "-d", "/data/", "-o", "capucine_shoe_sensors", "-c", "0", "-l", "WARNING"]
