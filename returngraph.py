import plotly.express as px
import json
import pandas as pd
from kaleido.scopes.plotly import PlotlyScope

scope = PlotlyScope(
    plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
    # plotlyjs="/path/to/local/plotly.js",
)
with open('C:/Users/Ольга/PycharmProjects/fastapi_clone/timeseries_rates.txt', 'r') as file:
    rates = json.load(file)['rates']
def sel_one_cur(cur_name):





    data = []

    for i in rates:
        data.append([i, rates[i][cur_name], cur_name])
    df = pd.DataFrame(data, columns=['Date', 'Rate', 'Currency'])

    fig = px.line(df, x='Date', y='Rate')
    with open("figure.png", "wb") as f:
        f.write(scope.transform(fig, format="png"))
cur = ["EUR", "UAH", "BYN"]
def take_percent_change_sev_cur(currencies):
    data = []
    start_date = '2022-03-15'
    for j in currencies:
        start_rate = rates[start_date][j]
        for i in rates:
            per_change = (rates[i][j] / start_rate - 1) * 100
            data.append([i, j, rates[i][j], per_change])
    df = pd.DataFrame(data, columns=['Date', 'Currency', 'Rate', 'Percent change'])
    fig = px.line(df, x='Date', y='Percent change', color='Currency')

    with open("C:/Users/Ольга/PycharmProjects/fastapi_clone/percent_changes.png", "wb") as p:
        p.write(scope.transform(fig, format="png"))

take_percent_change_sev_cur(cur)





