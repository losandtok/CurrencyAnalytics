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

        
def translate_date(start_day, start_month, start_year,end_day, end_month, end_year):
    if int(start_month) == 2:
        if int(start_year) % 4 == 0:
            if int(start_day) > 29:
                start_day = '29'
        else:
            if int(start_day) > 28:
                start_day = '28'
    elif (int(start_month) < 8 and int(start_month) % 2 == 0) or (int(start_month) > 7 and int(start_month) % 2 ==1):
        if int(start_day) > 30:
            start_day = '30'

    if int(end_month) == 2:
        if int(end_year) % 4 == 0:
            if int(end_day) > 29:
                end_day = '29'
        else:
            if int(end_day) > 28:
                end_day = '28'
    elif (int(end_month) < 8 and int(end_month) % 2 == 0) or (int(end_month) > 7 and int(end_month) % 2 ==1):
        if int(end_day) > 30:
            end_day = '30'
    return start_year + '-' + start_month + '-' + start_day, end_year + '-' + end_month + '-' + end_day


