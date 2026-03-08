import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

# Списък с твоите 4 линка (добавяме параметър за година 2020 директно в URL-а, ако е възможно, или филтрираме в кода)
URLS = [
    "https://occasion.sfa.bg/cars/search?slink=c9d14dd3eb2479f94fac86eec7e959cf",
    "https://occasion.sfa.bg/cars/search?slink=e5130b5b7e9ec35ad98c4ea3db21ec6b",
    "https://occasion.sfa.bg/cars/search?slink=1c91172309a8bbbb5453be192b0610b2",
    "https://occasion.sfa.bg/cars/search?slink=caa83f87cd748e53f0dacce2673fe0fa"
]

DB_FILE = "seen_ads.txt"

def get_ads():
    found_ads = []
    for url in URLS:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Намираме всички контейнери за коли (провери точния клас в сайта)
        items = soup.find_all('div', class_='car-item') # Примерно име на клас
        
        for item in items:
            title = item.find('h2').text.strip()
            link = item.find('a')['href']
            year_text = item.find('span', class_='year').text # Примерно
            
            # Филтър за година 2020+
            year = int(''.join(filter(str.isdigit, year_text)))
            if year >= 2020:
                found_ads.append(f"{title} ({year}) - {link}")
    return found_ads

def send_email(new_ads):
    msg = EmailMessage()
    msg.set_content("\n".join(new_ads))
    msg['Subject'] = f"Нови обяви Peugeot 2008 (4 сайта)"
    msg['From'] = os.environ['YAHOO_USER']
    msg['To'] = os.environ['YAHOO_USER']

    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
        smtp.login(os.environ['YAHOO_USER'], os.environ['YAHOO_PASS'])
        smtp.send_message(msg)

# Логика за проверка на нови обяви
def main():
    all_ads = get_ads()
    
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            seen = f.read().splitlines()
    else:
        seen = []

    new_ads = [ad for ad in all_ads if ad not in seen]

    if new_ads:
        send_email(new_ads)
        with open(DB_FILE, "a") as f:
            for ad in new_ads:
                f.write(ad + "\n")

if __name__ == "__main__":
    main()
