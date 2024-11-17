import requests
from bs4 import BeautifulSoup
import time
import json
import random
import urllib3
from zenrows import ZenRowsClient


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
# token = "75e993d477d041059b55be48206d589240b44bbc73b"
# proxyModeUrl = "http://{}:@proxy.scrape.do:8080".format(token)
proxy_list = [
    '79.137.39.50:80',
    '165.232.129.150:80',
    '198.74.51.79:8888',
    '43.134.68.153:3128'
]

# Select a random proxy
proxy = random.choice(proxy_list)

# Define the proxy
proxies = {
    'http': proxy,
    'https': proxy
}

letters = ["ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح",
           "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش",
           "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق",
           "ک", "گ", "ل", "م", "ن", "و", "ه", "ی"]

all_words = {}
for letter in letters:
    print(f'letter {letter} is started.')

    for page in range(1, 2):
        main_page_letter = f'https://abadis.ir/fatofa/?ch={letter}&pn={page}'


#main_page = 'https://abadis.ir/fatofa/?ch=ا&pn=1'
        try:
            main_page_detail = requests.get(main_page_letter)

            main_page_soup = BeautifulSoup(main_page_detail.text, 'html.parser')

            boxLi_div = main_page_soup.find('div', class_='boxLi')
            a_tags = boxLi_div.find_all('a') if boxLi_div else []

            words = [a_tag.get_text(strip=True) for a_tag in a_tags]
            print(f"Found words for letter '{letter}': {words}")

        except Exception as e:
            print(f"Failed to retrieve page {page} for letter '{letter}': {e}")
            continue

    client = ZenRowsClient("b886ab9d3e4611fda7b2a32feb9c0b1e4cfc359b")

    for word in words:
        try:
            every_page = f'https://abadis.ir/fatofa/{word}/'
            url = f'https://abadis.ir/fatofa/{word}/'
            # every_page = requests.get(every_page, proxies=proxies, verify=False, timeout=10)
            every_page = client.get(url)
            every_page_soup = BeautifulSoup(every_page.text, 'html.parser')
            meaning = every_page_soup.select_one('article')
            if meaning:
                for b_tag in meaning.find_all('b'):
                    b_tag.extract()

                meaning_text = meaning.get_text(strip=True)  # Get only the plain text
                print(meaning_text)
                all_words[word] = meaning_text
            
            else:
                print(f"No meaning found for '{word}'")
        except Exception as e:
                print(f"Error retrieving meaning for '{word}': {e}")
    
    print(f'Finished processing letter: {letter}')
    

with open("final.txt", 'w', encoding="utf-8",) as file:
    json.dump(all_words, file, ensure_ascii=False, indent=4)
