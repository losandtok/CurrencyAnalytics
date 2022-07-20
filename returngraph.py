import requests

import plotly.express as px
import pandas as pd
from kaleido.scopes.plotly import PlotlyScope

# Used to create DataFrame from Json dictionary containing currency rates in format dictionary with date-keys and
# values others dictionaries with currency code-keys and values rate in that day

import json

# Used to change Json format to dictionary


scope = PlotlyScope(
    plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
    # plotlyjs="/path/to/local/plotly.js",
)


# function take a list currencies and return graph with comparsion percent change them



def take_percent_change_sev_cur(currencies, start_date, end_date):
    url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}&base=USD"

    payload = {}
    headers = {
        "apikey": "nqVSc2eE3eoDiOYk3szQYL1ZQ5kPDBXH"
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    result = response.text
    rates = json.loads(result)['rates']
    temporary_data = []
    start_date = list(rates.keys())[0]

    # Fill temporary data tuples with date, name currency, rate and percent change
    for currency in currencies:
        start_rate = rates[start_date][currency]
        for date in rates:
            per_change = (rates[date][currency] / start_rate - 1) * -100
            temporary_data.append((date, currency, rates[date][currency], per_change))





    # Create pandas database from temporary data
    df = pd.DataFrame(temporary_data, columns=['Date', 'Currency', 'Rate', 'Percent change'])
    fig = px.line(df, x='Date', y='Percent change', color='Currency')

    with open("percent_changes.png", "wb") as p:
        p.write(scope.transform(fig, format="png"))



