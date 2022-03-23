from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import requests
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from config import CHROME_PROFILE_PATH

start = time.time()

today = date.today()
data_time = today.strftime("%d/%m/%Y")

city = {
    "abruzzo": 
	{
		"chieti": "22",
		"l-aquila": "6",
		"pescara": "62",
        "teramo": "88"
	},
    "basilicata":
    {
		"matera": "54",
		"potenza": "71"
	},
    "calabria":
    {
		"catanzaro": "29",
		"cosenza": "27",
        "crotone": "41",
		"reggio-calabria": "73",
        "vibo-valentia": "103"
	},
    "campania":
    {
		"avellino": "9",
		"benevento": "14",
        "caserta": "21",
		"napoli": "55",
        "salerno": "80"
	},
    "emilia-romagna":
    {
		"bologna": "15",
		"ferrara": "32",
        "forli-cesena": "31",
		"modena": "52",
        "parma": "67",
        "piacenza": "60",
		"ravenna": "72",
        "reggio-emilia": "74",
        "rimini": "78"
	},
    "friuli-venezia-giulia":
    {
		"gorizia": "37",
		"pordenone": "65",
        "trieste": "93",
		"udine": "95"
	},
    "lazio":
    {
		"frosinone": "35",
		"latina": "46",
        "rieti": "76",
		"roma": "77",
        "viterbo": "102"
	},
    "liguria":
    {
		"genova": "36",
		"imperia": "39",
        "la-spezia": "83",
		"savona": "86"
	},
    "lombardia":
    {
		"bergamo": "11",
		"brescia": "17",
        "como": "25",
		"cremona": "26",
        "lecco": "42",
		"lodi": "45",
        "mantova": "51",
		"milano": "50",
        "monza-brianza": "108",
		"pavia": "70",
        "sondrio": "82",
		"varese": "96"
	},
    "marche":
    {
		"ancona": "3",
		"ascoli-piceno": "5",
        "fermo": "109",
		"macerata": "48",
        "pesaro-urbino": "69"
	},
    "molise":
    {
		"campobasso": "20",
		"isernia": "40"
	},
    "piemonte":
    {
		"alessandria": "2",
		"asti": "8",
        "biella": "12",
		"cuneo": "24",
        "novara": "56",
        "torino": "90",
        "vercelli": "98"
	},
    "puglia":
    {
		"bari": "10",
        "brindisi": "16",
		"lecce": "43",
        "foggia": "33",
        "taranto": "87"
	},
    "sardegna":
    {
		"cagliari": "19",
		"nuoro": "57",
        "ogliastra": "105",
        "olbia-tempio": "104",
        "oristano": "58",
        "sassari": "85"
	},
    "sicilia":
    {
		"agrigento": "1",
		"caltanissetta": "23",
        "catania": "28",
		"enna": "30",
        "messina": "49",
        "palermo": "59",
        "ragusa": "75",
        "siracusa": "84",
        "trapani": "91"
	},
    "toscana":
    {
		"arezzo": "7",
		"firenze": "34",
        "grosseto": "38",
		"livorno": "44",
        "lucca": "47",
        "massa-carrara": "53",
        "pisa": "64",
        "pistoia": "68",
        "prato": "66",
        "siena": "81"
	},
    "trentino-alto-adige":
    {
		"bolzano": "18",
		"trento": "89"
	},
    "umbria":
    {
		"perugia": "63",
		"terni": "92"
	},
    "valle-d-aosta":
    {
		"aosta": "4"
	},
    "veneto":
    {
		"belluno": "13",
        "padova": "61",
        "rovigo": "79",
        "treviso": "94",
        "venezia": "99",
        "verona": "101",
        "vicenza": "100"
	}
}

##-FIRENZE-IMMOBILIARE##

for key, value in city.items():
    for i , num in value.items():

        #Erase contents of message file.txt
        file = open('city/%s/%s/msg_%s.txt' % (key,i,i), 'w')
             
        source_immo_firenze = requests.get("https://www.immobiliare.it/affitto-case/%s-provincia/?criterio=dataModifica&ordine=desc&prezzoMassimo=500"% (i)).text

        soup = BeautifulSoup(source_immo_firenze, 'lxml')

        while(True):
            for loop in soup.find_all('li', class_="nd-list__item in-realEstateResults__item"):
                try:
                    title = loop.find('a', class_="in-card__title")['title']
                    url_house = loop.find('a', class_="in-card__title")['href']
                    price = loop.find('li',class_="nd-list__item in-feat__item in-feat__item--main in-realEstateListCard__features--main").text

                    source_date = requests.get(url_house).text
                    soup_date = BeautifulSoup(source_date, 'lxml')

                    date_id_first = soup_date.findAll(class_="im-features__value")[0].text
                    date_id_second = soup_date.findAll(class_="im-features__value")[1].text

                    if data_time in date_id_first or data_time in date_id_second:
                        with open('city/%s/%s/msg_%s.txt' % (key,i,i), 'a') as f:
                            f.write(title + " 🏠 " + url_house + " 📱 " + price + " - " + data_time + "\n")
                
                except TypeError as te:
                    pass
                except AttributeError as ae:
                    pass           
            else:
                break

##-FIRENZE-SUBITO.IT##

        source_subito_firenze = requests.get("https://www.subito.it/annunci-%s/affitto/camere-posti-letto/%s/" % (key,i)).text

        soup = BeautifulSoup(source_subito_firenze, 'lxml')
        oggi = "Oggi"

        while(True):
            for loop in soup.find_all('div',class_="items__item BigCard-module_card__1pCxB"):
                try:
                    title = loop.find('h2', class_="index-module_sbt-text-atom__3a9r_ index-module_token-h6__3XGG_ size-normal index-module_weight-semibold__1Tjsf ItemTitle-module_item-title__39PNS BigCard-module_card-title__3l6LZ").text
                    url_house = loop.find('a', class_="BigCard-module_link__3TIKt")['href']            
                    price = loop.find('p',class_="index-module_price__2WXSC index-module_small__37iEO").get_text(" ")
                    date_today = loop.find('span', class_="index-module_sbt-text-atom__3a9r_ index-module_token-caption__1bBf_ index-module_size-small__3gqIP index-module_weight-semibold__1Tjsf index-module_date__1nkH_ index-module_with-spacer__3ZmrI").text
                    
                    if oggi in date_today:
                        with open('city/%s/%s/msg_%s.txt' % (key,i,i), 'a') as f:
                            f.write(title + " 🏠 " + url_house + " 📱 " + price + " - " + date_today + "\n")

                except TypeError as te:
                    pass
                except AttributeError as ae:
                    pass
            else:
                break

##-FIRENZE-MIOAFFITTO.IT##

        source_mioaffitto_firenze = requests.get("https://www.mioaffitto.it/search?provincia=%s&precio_max=600&order_field=1" % (num)).text
        
        soup = BeautifulSoup(source_mioaffitto_firenze, 'lxml')

        giorno, giorni = "giorno", "giorni"
        settimana, settimane = "settimana", "settimane"

        while(True):
            for loop in soup.find_all('li', class_="propertyCard"):
                try:
                    title = loop.find('a', class_= "qa-search-tituloCard-exist propertyCard__description--title")['title']
                    url_house = loop.find('a', class_="qa-search-tituloCard-exist propertyCard__description--title")['href']        
                    price = loop.find('span',class_="propertyCard__price--value").text.strip()
                    date_today = loop.find('span', class_="tagNew")['uib-tooltip']
                    
                    if not giorno in date_today:
                        if not giorni in date_today:
                            if not settimana in date_today:
                                if not settimane in date_today:
                                    with open('city/%s/%s/msg_%s.txt' % (key,i,i), 'a') as f:
                                        f.write(title + " 🏠 " + url_house + " 📱 " + price + " - " + date_today + "\n")

                except TypeError as te:
                    pass
                except AttributeError as ae:
                    pass
            else:
                break

end = time.time()
print(f"Runtime of the program is {end - start}")

##-WHATSAPP-##
"""
        with open('city/%s/%s/groups_%s.txt' % (key,i,i), 'r', encoding='utf8') as f:
                groups = [group.strip() for group in f.readlines()]

        with open('city/%s/%s/msg_%s.txt' % (key,i,i), 'r') as reader:
                messages = [message.strip() for message in reader.readlines()]

        options = webdriver.ChromeOptions()
        options.add_argument(CHROME_PROFILE_PATH)

        s=Service('/Users/admin/webdrivers/chromedriver')
        browser = webdriver.Chrome(service=s, options=options)

        browser.maximize_window()

        browser.get("https://web.whatsapp.com/")

        for message in messages:
            for group in groups:
                search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

                search_box = WebDriverWait(browser, 500).until(
                    EC.presence_of_element_located((By.XPATH, search_xpath)))
                
                search_box.clear()
                time.sleep(1)
                pyperclip.copy(group)

                search_box.send_keys(Keys.SHIFT,Keys.INSERT)

                time.sleep(2)

                group_xpath = f'//span[@title="{group}"]'
                group_title = browser.find_element(By.XPATH, group_xpath)
                group_title.click()

                time.sleep(1)

                input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'
                    
                input_box = browser.find_element(By.XPATH, input_xpath)
                    
                pyperclip.copy(message)
                    
                input_box.send_keys(Keys.SHIFT,Keys.INSERT)
                time.sleep(1)
                input_box.send_keys(Keys.ENTER)
                time.sleep(1)
        browser.close()
"""

# è piu veleoce a trovare la case che quando non trova i dati
# add folder city
# Restart python file every 24h

#-MAYBE-#

# Fix embeed message whatsapp ----> I can't unlikely let's wait next update
# Convert the code in executive file .exe --> Running in Server           

