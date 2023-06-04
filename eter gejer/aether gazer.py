import requests
from bs4 import BeautifulSoup
from lxml import html
import time
import urllib.parse
from tqdm import tqdm
import os

# URL of the webpage
def get_img(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the desired element using XPath
    element = soup.select_one('#mw-customcollapsible-角色立绘 table tbody tr:nth-of-type(2) td div div div div:nth-of-type(1) div div a')

    # Extract the image source from the element
    image_src = element['href']

    url = f'https://wiki.biligame.com{image_src}'
    # Print the image source
    # print(f)
    # Send a GET request to the webpage
    response = requests.get(url)

    # Parse the HTML content
    tree = html.fromstring(response.content)

    # Extract the href attribute using the XPath
    href = tree.xpath('string(//*[@id="file"]/a/@href)')
    return href
    # with open('output.txt', 'w') as file:
    #     file.writelines()

# get_img('https://wiki.biligame.com/dhmmr/%E4%BF%AE%E6%AD%A3%E8%80%85:%E6%97%A9%E6%A8%B1%E5%A4%A7%E5%9B%BD%E4%B8%BB')

with open('/workspaces/data-scraping/eter gejer/chara_list.txt', 'r') as file:
    lines = file.readlines()

# Process the lines and remove the characters after " | "
processed_lines = []
for line in lines:
    processed_line = line.split(' | ')[0]
    processed_lines.append(processed_line)
    
urls = []

for url in tqdm(processed_lines):
    url = urllib.parse.unquote(url)
    result = get_img(str(url)) + '\n'
    urls.append(result)
print(urls)
with open('output.txt', 'w') as file:
    file.writelines(urls)

print('done')