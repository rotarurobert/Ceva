FROM python

ADD main.py .
RUN pip install requests bs4 psycopg2-binary

CMD ["python",  "./main.py"] 
