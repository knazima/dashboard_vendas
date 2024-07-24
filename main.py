import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import calendar
import locale

#Importando dados_______________________________________________________________________________________________________
df = pd.read_csv('bases/dado_completos.csv')


#Criando App____________________________________________________________________________________________________________
app = dash.Dash(__name__)


#Montando Layout________________________________________________________________________________________________________
linha_titulo = html.Div([
    html.Div([
        dcc.Dropdown(
            id='dropdown_clientes',
            options=df['Cliente'].unique(),
            placeholder = 'Clientes',
            style={
                'font_family': 'Fira Code'


            }
        )
    ], style={'width':'25%'})
])



app.layout = html.Div([
    linha_titulo

])





#Callbacks______________________________________________________________________________________________________________



#Subindo servidor_______________________________________________________________________________________________________
if __name__ == '__main__': app.run_server(debug=True)