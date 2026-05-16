import urllib.request
import json

def get_exchange_rates():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        rates = data.get('rates', {})

        uah_rate = rates.get('UAH')
        eur_rate = rates.get('EUR')
        gbp_rate = rates.get('GBP')

        if not uah_rate:
            print("Не вдалося отримати курс гривні.")
            return

        print("📊 Актуальний курс валют:")
        print(f"💵 1 USD = {uah_rate:.2f} UAH")
        print(f"💶 1 EUR = {(uah_rate/eur_rate):.2f} UAH")
        print(f"💷 1 GBP = {(uah_rate/gbp_rate):.2f} UAH")

    except Exception as e:
        print(f"Помилка при отриманні даних: {e}")

if __name__ == "__main__":
    get_exchange_rates()
