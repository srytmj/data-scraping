import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import urllib.parse
from tqdm import tqdm
import os

def chara():
    url = "https://wiki.biligame.com/dhmmr/%E7%89%B9%E6%AE%8A:%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8?limit=500&ilsearch=%E8%A7%92%E8%89%B2%E5%A4%B4%E5%83%8F&user="
    urls = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> tags
    a_tags = soup.find_all("a")

    # Iterate over the <a> tags and extract href values
    for a_tag in a_tags:
        href = a_tag.get("href")
        
        # Check if the <a> tag contains the specified text and meets the conditions
        if href and "角色头像" in a_tag.text and ".png" in href and "钥从推荐" not in a_tag.text:
            result = f'https://wiki.biligame.com{href}'
            response = requests.get(result)

            # Parse the HTML content
            tree = html.fromstring(response.content)

            # Extract the href attribute using the XPath
            newhref = tree.xpath('string(//*[@id="file"]/a/@href)')
            newhref = f'{newhref}\n'
            urls.append(newhref)


    for url in urls:
        print(url)
    with open('/workspaces/data-scraping/eter gejer/data_chara.txt', 'w') as file:
        file.writelines(urls)

def sign_key():
    urls = []

    url = "https://wiki.biligame.com/dhmmr/%E7%89%B9%E6%AE%8A:%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8?limit=500&ilsearch=%E9%92%A5%E4%BB%8E%E5%A4%B4%E5%83%8F&user="

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> tags 
    a_tags = soup.find_all("a")

    # Iterate over the <a> tags and extract href values
    for a_tag in a_tags:
        href = a_tag.get("href")
        
        # Check if the <a> tag contains the specified text and meets the conditions
        if href and ".png" in href and "https://patchwiki.biligame.com" in href:
            print(href)
            result = f'{href}\n'
            urls.append(result)
    for url in urls:
        print(url)
    with open('/workspaces/data-scraping/eter gejer/data_sign.txt', 'w') as file:
        file.writelines(urls)

def sigil():
    url = "https://wiki.biligame.com/dhmmr/%E7%89%B9%E6%AE%8A:%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8?limit=500&ilsearch=%E5%88%BB%E5%8D%B0%E5%9B%BE%E6%A0%87&user="
    urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all <a> tags 
    a_tags = soup.find_all("a")

    # Iterate over the <a> tags and extract href values
    for a_tag in a_tags:
        href = a_tag.get("href")
        
        # Check if the <a> tag contains the specified text and meets the conditions
        if href and ".png" in href and "https://patchwiki.biligame.com" in href:
            print(href)
            result = f'{href}\n'
            urls.append(result)
    for url in urls:
        print(url)
    with open('/workspaces/data-scraping/eter gejer/data_sigil.txt', 'w') as file:
        file.writelines(urls)
# chara()
sign_key()
sigil()