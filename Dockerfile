FROM python

ADD main.py .

RUN pip install requests beautifulsoup4 psycopg2-binary

CMD ["python",  "./main.py"] 
