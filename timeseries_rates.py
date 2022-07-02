import requests



def set_timeseries(start_date, end_date):
    url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&base=USD"

    payload = {}
    headers= {
    "apikey": "nqVSc2eE3eoDiOYk3szQYL1ZQ5kPDBXH"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.text
    with open("timeseries_rates.txt", 'w') as file:
        file.seek(0)
        file.write(result)

