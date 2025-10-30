import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression

# Inicializar app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sales Analytics Dashboard"

# Carregar dados
df = pd.read_csv('data/sales_data.csv', parse_dates=['data'])

# Tratamento inicial dos dados
df['mes'] = df['data'].dt.to_period('M').astype(str)
df['ano'] = df['data'].dt.year

# Layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("📊 Sales Analytics Dashboard", className="text-center mb-4 mt-4"),
            html.Hr()
        ])
    ]),
    
    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Período:"),
            dcc.DatePickerRange(
                id='date-range',
                start_date=df['data'].min().date(),
                end_date=df['data'].max().date(),
                display_format='DD/MM/YYYY'
            )
        ], md=4),
        dbc.Col([
            html.Label("Categoria:"),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'Todas', 'value': 'all'}] + 
                        [{'label': cat, 'value': cat} for cat in df['categoria'].unique()],
                value='all',
                clearable=False
            )
        ], md=4),
        dbc.Col([
            html.Label("Região:"),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'Todas', 'value': 'all'}] + 
                        [{'label': reg, 'value': reg} for reg in df['regiao'].unique()],
                value='all',
                clearable=False
            )
        ], md=4)
    ], className="mb-4"),

    dcc.Store(id='filtered-data-store'),

    # KPIs
    dbc.Row(id='kpi-cards', className="mb-4"),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-evolution-chart'), md=12),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='category-sales-chart'), md=6),
        dbc.Col(dcc.Graph(id='top-products-chart'), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='region-heatmap'), md=6),
        dbc.Col(dcc.Graph(id='trend-analysis-chart'), md=6),
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='sales-forecast-chart'), md=12),
    ]),
    dbc.Row([
        dbc.Col(dbc.Button("Exportar para Excel", id="export-excel-button", color="success", className="mt-4"), md=2),
    ])

], fluid=True)


@app.callback(
    Output('filtered-data-store', 'data'),
    [
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'),
        Input('category-filter', 'value'),
        Input('region-filter', 'value')
    ]
)
def update_filtered_data(start_date, end_date, category, region):
    dff = df[
        (df['data'] >= pd.to_datetime(start_date)) & 
        (df['data'] <= pd.to_datetime(end_date))
    ]
    
    if category != 'all':
        dff = dff[dff['categoria'] == category]
    
    if region != 'all':
        dff = dff[dff['regiao'] == region]
        
    return dff.to_json(date_format='iso', orient='split')

@app.callback(
    Output('kpi-cards', 'children'),
    Input('filtered-data-store', 'data')
)
def update_kpi_cards(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    
    receita_total = dff['receita'].sum()
    total_vendas = dff['quantidade'].sum()
    ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0

    kpi_cards = [
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Receita Total", className="card-title"), html.P(f"R$ {receita_total:,.2f}", className="card-text")])), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Total de Vendas", className="card-title"), html.P(f"{total_vendas:,}", className="card-text")])), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([html.H4("Ticket Médio", className="card-title"), html.P(f"R$ {ticket_medio:,.2f}", className="card-text")])), md=4),
    ]
    return kpi_cards

@app.callback(
    Output('sales-evolution-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_sales_evolution_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    sales_evolution = dff.groupby(dff['data'].dt.to_period('M').astype(str))['receita'].sum().reset_index()
    sales_evolution_fig = px.line(sales_evolution, x='data', y='receita', title='Evolução de Vendas', labels={'data': 'Mês', 'receita': 'Receita'})
    sales_evolution_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return sales_evolution_fig

@app.callback(
    Output('category-sales-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_category_sales_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    category_sales = dff.groupby('categoria')['receita'].sum().reset_index()
    category_sales_fig = px.pie(category_sales, names='categoria', values='receita', title='Vendas por Categoria')
    category_sales_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return category_sales_fig

@app.callback(
    Output('top-products-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_top_products_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    top_products = dff.groupby('produto')['receita'].sum().nlargest(10).sort_values(ascending=True).reset_index()
    top_products_fig = px.bar(top_products, x='receita', y='produto', orientation='h', title='Top 10 Produtos por Receita')
    top_products_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return top_products_fig

@app.callback(
    Output('region-heatmap', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_region_heatmap(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    region_heatmap_data = dff.pivot_table(index='regiao', columns='categoria', values='receita', aggfunc='sum').fillna(0)
    region_heatmap_fig = px.imshow(region_heatmap_data, title='Mapa de Calor: Receita por Região e Categoria', labels=dict(x="Categoria", y="Região", color="Receita"))
    region_heatmap_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return region_heatmap_fig

@app.callback(
    Output('trend-analysis-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_trend_analysis_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    dff['data'] = pd.to_datetime(dff['data'])
    dff_trend = dff.copy()
    dff_trend['dias_desde_inicio'] = (dff_trend['data'] - dff_trend['data'].min()).dt.days
    daily_sales = dff_trend.groupby('dias_desde_inicio')['receita'].sum().reset_index()
    
    trend_fig = go.Figure()
    trend_fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=daily_sales['receita'], mode='markers', name='Vendas Diárias'))

    if len(daily_sales) > 1:
        X = daily_sales[['dias_desde_inicio']]
        y = daily_sales['receita']
        model = LinearRegression()
        model.fit(X, y)
        trend_line = model.predict(X)
        trend_fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=trend_line, mode='lines', name='Linha de Tendência', line=dict(color='red')))

    trend_fig.update_layout(title='Análise de Tendência de Vendas', xaxis_title='Dias desde o Início do Período', yaxis_title='Receita')
    trend_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return trend_fig

@app.callback(
    Output('sales-forecast-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_sales_forecast_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    dff['data'] = pd.to_datetime(dff['data'])
    dff_trend = dff.copy()
    dff_trend['dias_desde_inicio'] = (dff_trend['data'] - dff_trend['data'].min()).dt.days
    daily_sales = dff_trend.groupby('dias_desde_inicio')['receita'].sum().reset_index()
    
    forecast_fig = go.Figure()
    forecast_fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=daily_sales['receita'], mode='markers', name='Vendas Diárias'))

    if len(daily_sales) > 1:
        X = daily_sales[['dias_desde_inicio']]
        y = daily_sales['receita']
        model = LinearRegression()
        model.fit(X, y)
        
        # Prever próximos 30 dias
        future_days = np.arange(daily_sales['dias_desde_inicio'].max() + 1, daily_sales['dias_desde_inicio'].max() + 31).reshape(-1, 1)
        future_sales = model.predict(future_days)
        
        # Linha de tendência atual
        trend_line = model.predict(X)
        forecast_fig.add_trace(go.Scatter(x=daily_sales['dias_desde_inicio'], y=trend_line, mode='lines', name='Linha de Tendência', line=dict(color='red')))
        
        # Linha de previsão
        forecast_fig.add_trace(go.Scatter(x=future_days.flatten(), y=future_sales, mode='lines', name='Previsão (30 dias)', line=dict(color='green', dash='dash')))


    forecast_fig.update_layout(title='Previsão de Vendas (Próximos 30 dias)', xaxis_title='Dias desde o Início do Período', yaxis_title='Receita')
    forecast_fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    return forecast_fig

@app.callback(
    Output("export-excel-button", "n_clicks"),
    Input("export-excel-button", "n_clicks"),
    State('filtered-data-store', 'data'),
    prevent_initial_call=True,
)
def export_to_excel(n_clicks, filtered_data):
    if n_clicks > 0:
        dff = pd.read_json(filtered_data, orient='split')
        dff.to_excel("dados_exportados.xlsx", index=False)
        print("Dados exportados para dados_exportados.xlsx")
    return n_clicks

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)