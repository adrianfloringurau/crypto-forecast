import requests
import ai

def extract(coin, time, start_date, end_date):
    start = int(start_date.timestamp()*1000)
    end = int(end_date.timestamp()*1000)

    if (end < start):
        return None, None

    url = f'https://api.coincap.io/v2/assets/{coin.lower()}/history'
    apiKey = '308a82bd-93d7-432c-b848-0598cb6ccdb4'
    headers = {
        'Authorization': f'Bearer {apiKey}',
        'Content-Type': 'application/json'
    }
    params = {
        'interval': 'd1',
        'start': start,
        'end': end
    }

    data_response = requests.get(url, headers=headers, params=params)
    if data_response.status_code != 200:
        return None, None

    data = data_response.json()
    if "data" not in data:
        return None, None

    prices = data["data"]
    
    if len(prices) > 0:
        predicted_price, accuracy = ai.predict(prices, time)
    else:
        predicted_price = None
        accuracy = None
    return predicted_price, accuracy