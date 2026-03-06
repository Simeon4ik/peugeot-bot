import requests

def test_connection():
    url = "https://www.peugeot.bg"
    print(f"Проверявам връзката с {url}...")
    try:
        r = requests.get(url)
        print(f"Статус на сайта: {r.status_code} (200 означава ОК)")
    except Exception as e:
        print(f"Грешка при свързване: {e}")

if __name__ == "__main__":
    test_connection()
