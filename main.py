import requests
import time
import json
import threading
from playsound import playsound
from bs4 import BeautifulSoup


# Some pre-defined constants
interval = 120


# Collecting user data
number_of_urls = int(input("Введите количество ссылок (число), по которым будет происходить мониторинг: "))
url_array = []

for i in range(number_of_urls):
    url = input("Введите ссылку, по которой будет проходить мониторинг билетов: ").strip()
    url_array.append(url)


def work(url):
    """ Requesting JSON data (free seats) """
    print("Запускаем мониторинг: " + url) 

    # Fetching the data in order to get two states (old and new)
    while True:
        try:
            # Parsing the first (old) data
            old_page = requests.get(url)
            old_soup = BeautifulSoup(old_page.content, "html.parser")
            
            old_number_of_seats_text = old_soup.find("a", { "href" : url }).findChildren("div")[4].text
            if old_number_of_seats_text == "нет мест":
                old_number_of_seats = 0
            else:
                old_number_of_seats = int(old_number_of_seats_text.split()[0])

            time.sleep(interval)

            # Parsing the second (new) data
            new_page = requests.get(url)
            new_soup = BeautifulSoup(new_page.content, "html.parser")
            
            new_number_of_seats_text = new_soup.find("a", { "href" : url }).findChildren("div")[4].text
            if new_number_of_seats_text == "нет мест":
                new_number_of_seats = 0
            else:
                new_number_of_seats = int(new_number_of_seats_text.split()[0])

            if new_number_of_seats > old_number_of_seats:
                print("Новые билеты по " + url)

                for i in range(3):
                    playsound("success.mp3")
                    time.sleep(1) 
        except Exception:
            print("\n\n!!!ВОЗНИКЛА НЕИЗВЕСТНАЯ ОШИБКА!!!")

            for i in range(5):
                playsound("error.mp3")
                time.sleep(1)

            exit()


# Spawning our threads
for i in url_array:
    t = threading.Thread(target=work, args=(i,))
    t.start()
    time.sleep(1)
