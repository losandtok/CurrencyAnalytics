import json
import pandas as pd
def sel_one_cur(cur_name):
    import pandas as pd
    import plotly.express as px
    import json
    from kaleido.scopes.plotly import PlotlyScope
    scope = PlotlyScope(
        plotlyjs="https://cdn.plot.ly/plotly-latest.min.js",
        # plotlyjs="/path/to/local/plotly.js",
    )
    with open('timeseries_rates.txt', 'r') as file:
        rates = json.load(file)['rates']
    data = []

    for i in rates:
        data.append([i, rates[i][cur_name], cur_name])
    df = pd.DataFrame(data, columns=['Date', 'Rate', 'Currency'])

    fig = px.line(df, x='Date', y='Rate')
    with open("figure.png", "wb") as f:
        f.write(scope.transform(fig, format="png"))
with open('timeseries_rates.txt', 'r') as file:
    rates = json.load(file)['rates']
data = []
for i in rates:
    for j in rates[i]:
        data.append([i, j, rates[i][j]])
df = pd.DataFrame(data, columns=['Date', 'Currency', 'Rate'])

