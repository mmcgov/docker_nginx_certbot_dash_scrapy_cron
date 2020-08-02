#!/bin/sh
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth
import pandas as pd
import plotly
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
un_pw = [['user_1', 'pw_1'], ['un_2', 'pw_2'], ['un_3', 'pw_3']]
auth = dash_auth.BasicAuth(app, un_pw)
initial_country = 'Ireland'
data = pd.read_csv('/home/data/graph_data.csv', index_col='date')
intro = '''Interactive website analysing Covid-19 data.
           The data source is https://www.worldometers.info/coronavirus/'''
app.layout = html.Div(children=[html.H1(children='Covid 19 Data Analytics'),
                                dcc.Markdown(children=intro),
                                dcc.Dropdown(id='country',
                                options=[{'label': i, 'value': i} for i in
                                         list(set(data['country']))],
                                         value='Ireland'),
                                html.H4(id='live-update-text'),
                                dcc.Graph(id='main_graph',
                                          style={'width': 1000})
                                ])


def generate_table(dataframe, max_rows=10):
    """
    Function which generate dash table from dataframe

    Parameters:
    dataframe: pandas dataframe
    max_rows (int): number of rows to show from dataframe

    Returns
    dash table showing requested number of rows from dataframe
    """

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


@app.callback(Output('live-update-text', 'children'),
              [Input('country', 'value')])
def update_dataframe(value):
    """
    Dash function which updates data with chosen filter

    Parameters:
    value (str): chosen country to analyse
    max_rows (int): number of rows to show from dataframe

    Returns
    dash table showing requested number of rows from filtered dataframe
    """

    data = pd.read_csv('/home/data/graph_data.csv')
    data = data[data['country'] == value]
    date = data['date'].iloc[-1]
    country = data['country'].iloc[-1]
    tot_cases = data['total_cases'].iloc[-1]
    growth = round(data['case_growth_rate'].iloc[-1], 2)
    deaths = data['total_deaths'].iloc[-1]
    summary_dict = {'Date': [date],
                    'Country': [country],
                    'Total Cases': [tot_cases],
                    'Case growth rate': [f'{growth}%'],
                    'Total Deaths': [deaths]}
    summary_df = pd.DataFrame.from_dict(summary_dict)
    return generate_table(summary_df)


@app.callback(Output('main_graph', 'figure'), [Input('country', 'value')])
def update_graph(value):
    """
    Function which updates graph with chosen filter

    Parameters:
    value (str): chosen country to analyse

    Returns
    dash graph showing filtered data
    """

    graph_df = pd.read_csv('/home/data/graph_data.csv')
    graph_df = graph_df[graph_df['country'] == value]
    # Create the graph with subplots
    fig = plotly.tools.make_subplots(specs=[[{'secondary_y': True}]])
    fig['layout']['title'] = f'Cumulative total of Covid-19 cases in {value}\
                               along with daily rates of increase in new cases'
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 60, 't': 60
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.add_trace(go.Scatter(
                              x=graph_df['date'][-15:],
                              y=graph_df['total_cases'][-15:],
                              name='total cases'
                            ))

    fig.add_trace(go.Bar(
                         x=graph_df['date'][-15:],
                         y=graph_df['case_growth_rate'][-15:],
                         name='growth rate'),
                  secondary_y=True
                  )

    fig.show()
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port='8000')
