import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import sqlite3
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
app.layout = html.Div(
    [html.H1('Live Twitter Sentiment',style={'color': 'blue' ,'text-align': 'center'}),
     html.H2('Search:',style={'color': 'red'}),
     dcc.Input(id='sentiment_term', value='olympic', type='text'),
     dcc.Graph(id='live-graph', animate=True),
     dcc.Interval(
         id='graph-update',
         interval=1 * 1000
     ),
     ]
)


@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('graph-update', 'interval')])

def update_graph_scatter(sentiment_term):
    try:
        conn = sqlite3.connect('twitter.db')
        c = conn.cursor()
        words = sentiment_term.split(' ')
        print(words)
        frames = []
        for i in range(len(words)):
            frames.append(pd.read_sql("SELECT * FROM sentiment WHERE tweet LIKE ? ORDER BY unix DESC LIMIT 1000", conn,
                                      params=('%' + words[i] + '%',)))
        df = pd.concat(frames)
        df.sort_values('unix', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 5)).mean()
        df.dropna(inplace=True)

        df['date'] = pd.to_datetime(df['unix'], unit='ms')
        df.set_index('date', inplace=True)

        #df = df.resample('1min').mean()

        print(df['sentiment_smoothed'])
        df.to_csv("efabhvlek.csv")

        X = df.index
        Y = df.sentiment_smoothed.values

        data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode='lines',
            fill='tozeroy',
        )

        return {'data': [data],'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(range=[min(Y), max(Y)]))}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


if __name__ == '__main__':
    app.run_server(debug=True)
