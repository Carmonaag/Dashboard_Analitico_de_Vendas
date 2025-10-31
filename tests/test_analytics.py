
import pandas as pd
from utils.analytics import (
    calculate_kpis,
    get_sales_evolution,
    get_sales_by_category,
    get_top_products,
    get_region_heatmap_data,
    get_trend_analysis,
    get_sales_forecast,
)
from utils.data_processor import load_data, process_data


def test_calculate_kpis():
    """Testa o cálculo de KPIs."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    receita_total, total_vendas, ticket_medio = calculate_kpis(df)
    assert isinstance(receita_total, (int, float))
    assert isinstance(total_vendas, (int, float))
    assert isinstance(ticket_medio, (int, float))

def test_get_sales_evolution():
    """Testa a obtenção da evolução de vendas."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    sales_evolution = get_sales_evolution(df)
    assert isinstance(sales_evolution, pd.DataFrame)
    assert not sales_evolution.empty

def test_get_sales_by_category():
    """Testa a obtenção de vendas por categoria."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    sales_by_category = get_sales_by_category(df)
    assert isinstance(sales_by_category, pd.DataFrame)
    assert not sales_by_category.empty

def test_get_top_products():
    """Testa a obtenção do top 10 produtos."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    top_products = get_top_products(df)
    assert isinstance(top_products, pd.DataFrame)
    assert len(top_products) <= 10

def test_get_region_heatmap_data():
    """Testa a obtenção de dados para o mapa de calor por região."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    region_heatmap_data = get_region_heatmap_data(df)
    assert isinstance(region_heatmap_data, pd.DataFrame)
    assert not region_heatmap_data.empty

def test_get_trend_analysis():
    """Testa a obtenção da análise de tendência."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    daily_sales, trend_line = get_trend_analysis(df)
    assert isinstance(daily_sales, pd.DataFrame)
    assert trend_line is not None

def test_get_sales_forecast():
    """Testa a obtenção da previsão de vendas."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    daily_sales, trend_line, future_days, future_sales = get_sales_forecast(df)
    assert isinstance(daily_sales, pd.DataFrame)
    assert trend_line is not None
    assert future_days is not None
    assert future_sales is not None
