import time
import re
from bs4 import BeautifulSoup
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


cookie_list=[{"Domain":".anime-kage.eu","expirationDate":"1722439827","hostOnly":"false","HttpOnly":"false","name":"_ga","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"GA1.2.1239640000.1654621532"},{"Domain":".anime-kage.eu","expirationDate":"1686159346.329137","hostOnly":"false","HttpOnly":"false","name":"usr","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"Dariusx"},{"Domain":".anime-kage.eu","expirationDate":"1686159346.329165","hostOnly":"false","HttpOnly":"false","name":"usri","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"39989"},{"Domain":".anime-kage.eu","expirationDate":"1686159346.329174","hostOnly":"false","HttpOnly":"false","name":"usrs","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"39989629f8c72bc73d8.08207493"},{"Domain":".anime-kage.eu","expirationDate":"1659454227","hostOnly":"false","HttpOnly":"false","name":"_gid","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"GA1.2.1790831797.1658659233"},{"Domain":".anime-kage.eu","expirationDate":"1692547393","hostOnly":"false","HttpOnly":"false","name":"__gads","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"ID=093d5f48c4e2ff91-229c647edacd0020:T=1658851393:RT=1658851393:S=ALNI_MYZklepPaNHr5I6UtdZ0wTn3PzQjA"},{"Domain":"ak497.anime-kage.eu","hostOnly":"true","HttpOnly":"false","name":"PHPSESSID","path":"/","sameSite":"Lax","Secure":"false","session":"true","storeId":"0","value":"rf0mbuit1rkbi2b95th3urrsud"},{"Domain":"ak497.anime-kage.eu","expirationDate":"1690873447.286612","hostOnly":"true","HttpOnly":"false","name":"cdd","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"1"},{"Domain":".anime-kage.eu","expirationDate":"1690903827","hostOnly":"false","HttpOnly":"false","name":"lastVisit","path":"/","sameSite":"Lax","Secure":"false","session":"false","storeId":"0","value":"1659367827"}]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_prefs = {}
chrome_options.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = {"images": 2}
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://ak496.anime-kage.eu')

for cookie in cookie_list:
        driver.add_cookie(cookie)


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
        # Connect to the URL
        driver.get(url+'/'+str(episode))
        time.sleep(1)
        #print(url+'/'+str(episode))

        # Parse HTML and save to BeautifulSoup object¶
        soup = BeautifulSoup(driver.page_source, "html.parser")

        found_fembed = ''
        found_mega = ''
        found_lare = ''
        found_up=''
        found_sendvid = ''
        found_vtube = ''

        for one_a_tag in soup.findAll('iframe'):
            if one_a_tag.get('data-src'):
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
driver.close()
