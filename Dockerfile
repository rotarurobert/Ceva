FROM ubuntu

ADD main.py .

RUN apt-get update -y

RUN apt-get install -y autoconf \
                       build-essential \
                       curl \
                       git \
                       vim-tiny

# Python dependencies
RUN apt-get install -y python \
                       python-dev \
                       python-distribute \
                       python-pip \
                       ipython


RUN pip install requests_html bs4 psycopg2-binary

CMD ["python",  "./main.py"] 
