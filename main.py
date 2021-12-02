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

    current_number_of_seats = 0

    while True:
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            
            number_of_seats_text = soup.find("a", { "href" : url }).findChildren("div")[4].text
            if number_of_seats_text == "нет мест":
                number_of_seats = 0
            else:
                number_of_seats = int(number_of_seats_text.split()[0])
            
            if number_of_seats > current_number_of_seats:
                current_number_of_seats = number_of_seats
                print("Новые билеты по " + url)

                for i in range(3):
                    playsound("success.mp3")
                    time.sleep(1)

            time.sleep(interval)
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
