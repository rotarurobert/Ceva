FROM ubuntu

ADD main.py .

RUN apt-get update -y

RUN apt-get install -y autoconf \
                       build-essential \
                       curl \
                       git \
                       vim-tiny

# Python dependencies
RUN apt-get install -y python3 \
                       python3-dev \
                       python3-distribute \
                       python3-pip

RUN pip install requests_html bs4 psycopg2-binary

CMD ["python",  "./main.py"] 
