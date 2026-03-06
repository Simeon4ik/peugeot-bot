import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

# Настройки от GitHub Secrets
EMAIL_USER = os.environ.get('EMAIL_USER') # Твоят Yahoo имейл
EMAIL_PASS = os.environ.get('EMAIL_PASS') # 16-цифреният код от Yahoo
TARGET_EMAIL = "simeon.d.ralchev@gmail.com"

def check_for_cars():
    url = "https://search.peugeot.bg"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Намираме всички линкове към отделни обяви
        # Обикновено са в 'a' тагове вътре в артикули или карти
        car_links = soup.select('a[href*="/used-cars/"]') 
        
        seen_links = set()
        for link in car_links:
            href = link.get('href')
            if href and "/used-cars/" in href:
                full_url = href if href.startswith('http') else f"https://search.peugeot.bg{href}"
                
                if full_url not in seen_links:
                    print(f"Намерен линк: {full_url}")
                    send_email(full_url)
                    seen_links.add(full_url)
                    
    except Exception as e:
        print(f"Грешка при сканиране: {e}")

def send_email(car_url):
    msg = EmailMessage()
    msg['Subject'] = 'Нова обява за Peugeot!'
    msg['From'] = EMAIL_USER
    msg['To'] = TARGET_EMAIL
    msg.set_content(f'Намерена е нова кола. Виж детайлите тук:\n\n{car_url}')

    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"Имейлът е изпратен до {TARGET_EMAIL}")
    except Exception as e:
        print(f"Грешка при пращане на имейл: {e}")

if __name__ == "__main__":
    check_for_cars()
