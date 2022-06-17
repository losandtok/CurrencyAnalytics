import requests
import json
import plotly.express as px
from kaleido.scopes.plotly import PlotlyScope

scope = PlotlyScope(
    plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
    # plotlyjs="/path/to/local/plotly.js",
)


def take_month_data(month):
  dates = []
  results = []
  if month < 10:
    month = '0' + str(month)
  for i in range(1, 31):

    if i < 10:
      i = "0" + str(i)
    url = f"https://api.apilayer.com/exchangerates_data/convert?date=2022-{month}-{i}&to=USD&from=EUR&amount=1"

    payload = {}
    headers= {
      "apikey": "REvWVtnZpX0myHmD8qw4MRuRMi0un076"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.text
    result = json.loads(result)
    dates.append(result['date'])
    results.append(result['result'])
  return dates, results
may_dates, may_results = take_month_data(5)

fig = px.line(x=may_dates, y=may_results)
with open("figure.png", "wb") as f:
  f.write(scope.transform(fig, format="png"))
