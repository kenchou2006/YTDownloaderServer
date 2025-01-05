FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CHROME_BIN /usr/bin/chromium
ENV CHROME_DRIVER /usr/bin/chromium-driver
ENV CHROME_USER_DATA_DIR /root/.config/chromium
ENV DISPLAY=:99

RUN apt-get update && apt-get install -y chromium

RUN mkdir -p /root/.config/chromium

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["bash", "-c", "Xvfb :99 & python3 /app/fetchCookies/main.py && gunicorn web.wsgi:application --bind :8000 -k gevent"]