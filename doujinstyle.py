import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

while True:
    def connect():
        url = 'https://doujinstyle.com/?p=search&source=1&type=artist&result=%E3%83%91%E3%83%B3%E9%87%8E%E5%AE%9F%E3%80%85%E7%BE%8E'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        gridDetails = soup.select(".gridDetails")
        return gridDetails

    gridDetails = connect()
    if gridDetails == []:
        gridDetails = connect()
       
    print("============== SCRAPPED ==============")

    i = 0
    for x in gridDetails:
        i += 1
        numa = 0
        datas = []


        for item in x:
            tags = []
            item = str(item)

            if numa == 1 : # url & album

                url = (f"https://doujinstyle.com/?p=page&type=1&id={item[37:42]}")

                item = re.sub(r'\<a.+title=\"','',item)
                item = re.sub(r'\">.+\>','',item)

                datas.append(url)
                datas.append(item)  

            if numa == 4 : # artist
                item = re.sub(r'\<a.+result=','',item)
                item = re.sub(r'\".+\>','',item)
                item = urllib.parse.unquote(item)
                datas.append(item)

            if numa == 8 : # tags

                item = re.sub(r'\<s.+s\"\/\>','',item)
                item = re.sub(r'\<\/s.+>','',item)

                new_data = item.split(",")
                num = 0
                for x in new_data:
                    x = re.sub(r'\<a.+result=','',x)
                    x = re.sub(r'\".+\>','',x)
                    
                    if num != 0:
                        tags.append(x[1:])
                    else:
                        tags.append(x)

                    num += 1

                datas.append(tags)
            numa += 1

            if numa == 11:
                with open('result.txt', 'a', encoding="utf-8") as f:
                    f.write(''.join(f"URL : {datas[0]}\nArtist : {datas[2]}\nAlbum : {datas[1]}\nGenre : {', '.join(str(e) for e in datas[3])}\n\n"))                    # for x in datas:
                    #     f.write(f"{x}\n")
                print(f"{datas[0]} added")
                # print(f"URL : {datas[0]}\nArtist : {datas[2]}\nAlbum : {datas[1]}\nGenre : {', '.join(str(e) for e in datas[3])}")
            
        datas.clear()

    break