import plotly.express as px
import pandas as pd
from kaleido.scopes.plotly import PlotlyScope
#Used to create DataFrame from Json dictonary containing currency rates in format dictionary with date-keys and values others dicionaries with currency code-keys and values rate in that day



import json
#Used to change Json format to dictionary


scope = PlotlyScope(
    plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
    # plotlyjs="/path/to/local/plotly.js",
)

with open('C:/Users/Ольга/PycharmProjects/fastapi_clone/timeseries_rates.txt', 'r') as file:
    rates = json.load(file)['rates']

#function take a list currencies and return graph with comparsion percent change them
def take_percent_change_sev_cur(currencies):
    temporary_data = []
    start_date = '2022-03-15'

    #Fill temporary data tuples with date, name currency, rate and percent change
    for currency in currencies:
        start_rate = rates[start_date][currency]
        for date in rates:
            per_change = (rates[date][currency] / start_rate - 1) * 100
            temporary_data.append((date, currency, rates[date][currency], per_change))


    #Create pandas database from tempora
    df = pd.DataFrame(temporary_data, columns=['Date', 'Currency', 'Rate', 'Percent change'])
    fig = px.line(df, x='Date', y='Percent change', color='Currency')

    with open("C:/Users/Ольга/PycharmProjects/fastapi_clone/percent_changes.png", "wb") as p:
        p.write(scope.transform(fig, format="png"))

take_percent_change_sev_cur(['EUR', 'UAH', 'PLN'])





