
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd

from components.charts import (
    create_category_sales_chart,
    create_region_heatmap,
    create_sales_evolution_chart,
    create_sales_forecast_chart,
    create_top_products_chart,
    create_trend_analysis_chart,
)
from components.filters import (
    create_category_filter,
    create_date_range_filter,
    create_region_filter,
)
from components.kpi_cards import create_kpi_card
from components.tables import create_data_table
from utils.analytics import (
    calculate_kpis,
    get_region_heatmap_data,
    get_sales_by_category,
    get_sales_evolution,
    get_sales_forecast,
    get_top_products,
    get_trend_analysis,
)
from utils.data_processor import load_data, process_data
from utils.cache import get_from_cache, set_to_cache, get_cache_key

# Inicializar app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sales Analytics Dashboard"

# Carregar e processar dados
df = load_data('data/sales_data.csv')
df = process_data(df)

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
        dbc.Col([html.Label("Período:"), create_date_range_filter(df)], md=4),
        dbc.Col([html.Label("Categoria:"), create_category_filter(df)], md=4),
        dbc.Col([html.Label("Região:"), create_region_filter(df)], md=4)
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
    
    # Tabela de Dados
    dbc.Row([
        dbc.Col(html.Div(id='data-table-container'), md=12)
    ], className="mt-4"),

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
    filters = {
        'start_date': start_date,
        'end_date': end_date,
        'category': category,
        'region': region
    }
    cache_key = get_cache_key(filters)
    
    cached_data = get_from_cache(cache_key)
    
    if cached_data is not None:
        return cached_data.to_json(date_format='iso', orient='split')

    dff = df[
        (df['data'] >= pd.to_datetime(start_date)) & 
        (df['data'] <= pd.to_datetime(end_date))
    ]
    
    if category != 'all':
        dff = dff[dff['categoria'] == category]
    
    if region != 'all':
        dff = dff[dff['regiao'] == region]
    
    set_to_cache(cache_key, dff)
        
    return dff.to_json(date_format='iso', orient='split')

@app.callback(
    Output('data-table-container', 'children'),
    Input('filtered-data-store', 'data')
)
def update_data_table(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    return create_data_table(dff)

@app.callback(
    Output('kpi-cards', 'children'),
    Input('filtered-data-store', 'data')
)
def update_kpi_cards(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    receita_total, total_vendas, ticket_medio = calculate_kpis(dff)
    
    kpi_cards = [
        create_kpi_card("Receita Total", receita_total),
        create_kpi_card("Total de Vendas", total_vendas, formatter=lambda x: f"{x:,}"),
        create_kpi_card("Ticket Médio", ticket_medio),
    ]
    return kpi_cards

@app.callback(
    Output('sales-evolution-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_sales_evolution_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    sales_evolution = get_sales_evolution(dff)
    return create_sales_evolution_chart(sales_evolution)

@app.callback(
    Output('category-sales-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_category_sales_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    category_sales = get_sales_by_category(dff)
    return create_category_sales_chart(category_sales)

@app.callback(
    Output('top-products-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_top_products_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    top_products = get_top_products(dff)
    return create_top_products_chart(top_products)

@app.callback(
    Output('region-heatmap', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_region_heatmap(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    region_heatmap_data = get_region_heatmap_data(dff)
    return create_region_heatmap(region_heatmap_data)

@app.callback(
    Output('trend-analysis-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_trend_analysis_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    daily_sales, trend_line = get_trend_analysis(dff)
    return create_trend_analysis_chart(daily_sales, trend_line)

@app.callback(
    Output('sales-forecast-chart', 'figure'),
    Input('filtered-data-store', 'data')
)
def update_sales_forecast_chart(filtered_data):
    dff = pd.read_json(filtered_data, orient='split')
    daily_sales, trend_line, future_days, future_sales = get_sales_forecast(dff)
    return create_sales_forecast_chart(daily_sales, trend_line, future_days, future_sales)

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
