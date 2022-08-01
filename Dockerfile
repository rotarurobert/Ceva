FROM ubuntu

ADD main.py .

RUN apt-get update
RUN apt install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget libgbm1

RUN apt install -y python3 python3-pip
RUN apt-get -y install xvfb
RUN apt-get -y install gtk2-engines-pixbuf
RUN apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable
RUN apt-get -y install imagemagick x11-apps
RUN Xvfb -ac :99 -screen 0 1280x1024x16 & export DISPLAY=:99

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# # It won't run from the root user.
# RUN groupadd chrome && useradd -g chrome -s /bin/bash -G audio,video chrome \
#     && mkdir -p /home/chrome && chown -R chrome:chrome /home/chrome



RUN pip3 install -U selenium
RUN pip3 install bs4 psycopg2-binary webdriver_manager

CMD ["python3",  "./main.py"] 
