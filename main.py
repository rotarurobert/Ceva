import time
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import psycopg2

session = HTMLSession()

root_url = 'https://ak447.anime-kage.eu/ak/anime/'

conn=psycopg2.connect(
    database="exampledb",
    user="docker",
    password="docker",
    host="database"
)

cur = conn.cursor()
cur.execute ('select * from "tblShows" where name <> \'One Piece\'')
showRows= cur.fetchall()
for showRow in showRows:
    url=root_url+re.sub('[^a-zA-Z0-9 \-\n\.]', '',showRow[1]).strip().replace(' ','-').lower()
    end=int(showRow[2])
    start=1
    for episode in range(start,end+1):
        time.sleep(0.3)
        # Connect to the URL
        response = session.get(url+'/'+str(episode))
        response.html.render()
        #print(url+'/'+str(episode))

        # Parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(response.text, "html.parser")

        found_fembed = ''
        found_mega = ''
        found_lare = ''
        found_up=''
        found_sendvid = ''
        found_vtube = ''

        for one_a_tag in soup.findAll('iframe'):
            if "fembed" in one_a_tag.get('data-src'):
                found_fembed = one_a_tag.get('data-src')
            elif "mega.nz" in one_a_tag.get('data-src'):
                found_mega = one_a_tag.get('data-src')
            elif "vtube.to" in one_a_tag.get('data-src'):
                found_vtube = one_a_tag.get('data-src')
            elif "streamlare.com" in one_a_tag.get('data-src'):
                found_lare = one_a_tag.get('data-src')
            elif "upstream.to" in one_a_tag.get('data-src'):
                found_up = one_a_tag.get('data-src')
            elif "sendvid.com" in one_a_tag.get('data-src'):
                found_up = one_a_tag.get('data-src')

        if found_fembed:
            cur.execute("insert into \"tblLinks\" (show_id,episode,link,downloaded) VALUES ("+str(showRow[0])+","+str(episode)+",\'"+found_fembed+"\',FALSE)")
            print(found_fembed)
        elif found_mega:
            cur.execute("insert into \"tblLinks\" (show_id,episode,link,downloaded) VALUES ("+str(showRow[0])+","+str(episode)+",\'"+found_mega+"\',FALSE)")
            print(found_mega)
        elif found_vtube:
            cur.execute("insert into \"tblLinks\" (show_id,episode,link,downloaded) VALUES ("+str(showRow[0])+","+str(episode)+",\'"+found_vtube+"\',FALSE)")
            print(found_vtube)
        elif found_up:
            cur.execute("insert into \"tblLinks\" (show_id,episode,link,downloaded) VALUES ("+str(showRow[0])+","+str(episode)+",\'"+found_up+"\',FALSE)")
            print(found_up)
        elif found_lare:
            cur.execute("insert into \"tblLinks\" (show_id,episode,link,downloaded) VALUES ("+str(showRow[0])+","+str(episode)+",\'"+found_lare.replace('/e/','/v/')+"\',FALSE)")
            print(found_lare)

conn.commit()
cur.close()
conn.close()

