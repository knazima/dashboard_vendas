import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash_bootstrap_templates import ThemeSwitchAIO
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import calendar
import locale

#Variáveis de apoio_____________________________________________________________________________________________________
dark_tema = 'darkly'
vapor_tema = 'vapor'
url_dark = dbc.themes.DARKLY
url_vapor = dbc.themes.VAPOR


#Importando dados_______________________________________________________________________________________________________
df = pd.read_csv('bases/dado_completos.csv')

df['dt_Venda']=pd.to_datetime(df['dt_Venda'])

df['Mês'] = df['dt_Venda'].dt.strftime('%b').str.upper()


#Funções de apoio_______________________________________________________________________________________________________

def filtro_cliente(cliente_selecionado):
    if cliente_selecionado is None:
        return pd.Series(True, index=df.index)
    else:
        return df['Cliente'] == cliente_selecionado


def filtro_mes(mes_selecionado):
    if mes_selecionado is None:
        return pd.Series(True, index=df.index)
    return df['Mês'] == mes_selecionado

def filtro_categoria(categoria_selecionada):
    if categoria_selecionada is None:
        return pd.Series(True, index=df.index)
    else:
        return df['id_Categoria'] == categoria_selecionada


#Criando App____________________________________________________________________________________________________________
app = dash.Dash(__name__)


#Montando Layout________________________________________________________________________________________________________
linha_cabecalho = html.Div([
    html.Div([
        dcc.Dropdown(
            id='dropdown_clientes',
            options=df['Cliente'].unique(),
            placeholder = 'Clientes',
            style={
                'font_family': 'Fira Code',
                'color': '#101010'

            }
        )
    ], style={'width':'25%'}), 

    html.Div(
        html.Legend(
            'DoReMi Store',
            style={'font-size': '150%', 'text-align': 'center'}
        ),
        style={'width': '50%'}
    ),
    html.Div(
        ThemeSwitchAIO(
            aio_id='theme',
            themes=[
                url_dark,
                url_vapor                
            ]
        ), style ={'width': '25%'}
    )
], style={
    'text-align': 'center',
    'display': 'flex',
    'justify-content': 'space-between',
    'align-items': 'center',
    'margin-top': '20px'
})


linha_1 = html.Div([
    html.Div([
        html.H4(id='output_cliente'),
        dcc.Graph(id='visual01')
    ],
    style={'text-align': 'center', 'width': '65%'}
    ),

    html.Div(
        dbc.RadioItems(
            id='radio_meses', 
            options=df['Mês'].unique(),
            inline = True
        ), style = {'width': '30%'}
    ),

    html.Div([
        dbc.RadioItems(
            id='radio_categoria',
            options=df['Categorias'].unique(),
            inline=True
        )
    ])
], style={'margin-top':'40px',
          'display':'flex',
          'justify-content': 'space-around',
          'height': '300px'}
          )



app.layout = html.Div([
    linha_cabecalho,
    linha_1

])





#Callbacks______________________________________________________________________________________________________________
@app.callback(
        Output('output_cliente', 'children'),
        Input('dropdown_clientes', 'value')

)

def atualizar_txt(cliente_selecionado):
    if cliente_selecionado:
        return f'Top5 Produtos comprados por: {cliente_selecionado}'
    return 'Top5 Produtos vendidos!'


@app.callback(
    Output('visual01', 'figure'),
    [
        Input('dropdown_clientes','value'),
        Input('radio_meses', 'value'),
        Input('radio_categoria', 'value'),
        Input(ThemeSwitchAIO.ids.switch('theme'), 'value')
    ]
)
def visual01(cliente, mes, categoria,toggle):

    template = dark_tema if toggle else vapor_tema

#     if toggle:
#     template = dark_tema
# else:
#     template = vapor_tema

    nome_cliente = filtro_cliente(cliente)
    nome_mes = filtro_mes(mes)
    nome_categoria = filtro_categoria(categoria)

    filtros = nome_cliente & nome_mes & categoria

    df1 = df.loc[filtros]

    df_grupo = df1.groupby(['Produto','Categorias'])['Total'].sum().reset_index()
    df_top5=df_grupo.sort_values(by='Total', ascending=False).head(5)

    fig1 = px.bar(
        df_top5,
        x='Produto',
        y='Total',
        text='Total',
        color_continuous_scale = 'Blues',
        height=280,
        template=template
    )

    fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    fig1.update_layout(
        margin={'t':0},
        xaxis = {'showgrid': False},
        yaxis = {
            'showgrid': False,
            'range': [df_top5['Total'].min()*0, 
                      df_top5['Total'].max()*1.2]
        },
        xaxis_title=None,
        yaxis_title=None,
        xaxis_tickangle=-15,
        font={'size':13},
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0)'
                
    )
    return fig1



#Subindo servidor_______________________________________________________________________________________________________
if __name__ == '__main__': app.run_server(debug=True)