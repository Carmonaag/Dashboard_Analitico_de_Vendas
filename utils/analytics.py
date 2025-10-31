
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def calculate_kpis(dff):
    """Calcula os KPIs de vendas."""
    receita_total = dff['receita'].sum()
    total_vendas = dff['quantidade'].sum()
    ticket_medio = receita_total / total_vendas if total_vendas > 0 else 0
    return receita_total, total_vendas, ticket_medio

def get_sales_evolution(dff):
    """Retorna a evolução das vendas ao longo do tempo."""
    return dff.groupby(dff['data'].dt.to_period('M').astype(str))['receita'].sum().reset_index()

def get_sales_by_category(dff):
    """Retorna as vendas por categoria."""
    return dff.groupby('categoria')['receita'].sum().reset_index()

def get_top_products(dff):
    """Retorna os 10 produtos mais vendidos."""
    return dff.groupby('produto')['receita'].sum().nlargest(10).sort_values(ascending=True).reset_index()

def get_region_heatmap_data(dff):
    """Retorna os dados para o mapa de calor de vendas por região."""
    return dff.pivot_table(index='regiao', columns='categoria', values='receita', aggfunc='sum').fillna(0)

def get_trend_analysis(dff):
    """Retorna a análise de tendência de vendas."""
    dff['data'] = pd.to_datetime(dff['data'])
    dff_trend = dff.copy()
    dff_trend['dias_desde_inicio'] = (dff_trend['data'] - dff_trend['data'].min()).dt.days
    daily_sales = dff_trend.groupby('dias_desde_inicio')['receita'].sum().reset_index()

    if len(daily_sales) > 1:
        X = daily_sales[['dias_desde_inicio']]
        y = daily_sales['receita']
        model = LinearRegression()
        model.fit(X, y)
        trend_line = model.predict(X)
        return daily_sales, trend_line
    return daily_sales, None

def get_sales_forecast(dff):
    """Retorna a previsão de vendas para os próximos 30 dias."""
    dff['data'] = pd.to_datetime(dff['data'])
    dff_trend = dff.copy()
    dff_trend['dias_desde_inicio'] = (dff_trend['data'] - dff_trend['data'].min()).dt.days
    daily_sales = dff_trend.groupby('dias_desde_inicio')['receita'].sum().reset_index()

    if len(daily_sales) > 1:
        X = daily_sales[['dias_desde_inicio']]
        y = daily_sales['receita']
        model = LinearRegression()
        model.fit(X, y)

        future_days = np.arange(daily_sales['dias_desde_inicio'].max() + 1, daily_sales['dias_desde_inicio'].max() + 31).reshape(-1, 1)
        future_sales = model.predict(future_days)
        trend_line = model.predict(X)

        return daily_sales, trend_line, future_days, future_sales
    return daily_sales, None, None, None
