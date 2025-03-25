import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load the csv file then count the wins per country
df = pd.read_csv('worldcup_data.csv')

wins = df["Winner"].value_counts().reset_index()
wins.columns = ["Country","Wins"]

# Creating Choropleth Map
choropleth_map = px.choropleth(
    wins,
    locations = "Country",
    locationmode = "country names",
    color = "Wins",
    title = "FIFA World Cup Wins",
    color_continuous_scale = "Inferno",
    width = 1000,
    height = 750
)
choropleth_map.show()

# Dash
app = Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("FIFA World Cup Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(id="choropleth", figure=choropleth_map),
    dcc.Dropdown(
        id='country-dropdown',
        options = [{'label': c, 'value': c} for c in sorted(wins["Country"].unique())],
        value='Brazil',
        style={'width': '50%'}
    ),
    html.Div(id='country-wins'),
    html.H2("Select a Year: "),
    dcc.Dropdown(
        id='year-dropdown',
        options = [{'label': str(y), 'value': y} for y in df["Year"]],
        value = 2022,
        style={'width' : '50%'}
    ),
    html.Div(id='year-results')
])

@app.callback(
    Output('country-wins', 'children'),
    Input('country-dropdown', 'value')
)

def country_wins(country):
    total_wins = wins[wins["Country"] == country]["Wins"].values
    if total_wins.size > 0:
        return f"{country} has won the World Cup {total_wins[0]} time(s)."
    return f"{country} has never won the World Cup."

@app.callback(
    Output('year-results', 'children'),
    Input('year-dropdown', 'value')
)

def year_results(year):
    match = df[df["Year"] == year]
    if not match.empty:
        winner = match["Winner"].values[0]
        runner_up = match["Runner-Up"].values[0]
        return f"In the year {year}, {winner} beat {runner_up}."
    return "The World Cup didn't happen that year."

if __name__ == '__main__':
    app.run_server(debug=True)
