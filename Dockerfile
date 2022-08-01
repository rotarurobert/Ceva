FROM python:3.8.13-slim-buster

ADD main.py .

RUN pip install requests_html bs4 psycopg2-binary

CMD ["python",  "./main.py"] 
