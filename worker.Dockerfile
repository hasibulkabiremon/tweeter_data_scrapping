FROM dorowu/ubuntu-desktop-lxde-vnc:focal

WORKDIR /app
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y google-chrome-stable
RUN sudo apt-get install -y fonts-beng fonts-beng-extra fonts-lohit-beng-bengali
RUN sudo apt install -y python3-pip
RUN sudo apt-get install -y python3-tk
RUN apt-get install cron
RUN apt install -y git
RUN apt install -y pkg-config
RUN apt install -y libcairo2-dev libjpeg-dev libgif-dev
ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Dhaka
COPY ./scraper.conf /etc/supervisor/conf.d/scraper.conf
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY ./ /app
RUN touch /var/log/cron.log
CMD cron -f