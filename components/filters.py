
from dash import dcc
import pandas as pd

def create_date_range_filter(df):
    """Cria o filtro de período."""
    return dcc.DatePickerRange(
        id='date-range',
        start_date=df['data'].min().date(),
        end_date=df['data'].max().date(),
        display_format='DD/MM/YYYY'
    )

def create_category_filter(df):
    """Cria o filtro de categoria."""
    return dcc.Dropdown(
        id='category-filter',
        options=[{'label': 'Todas', 'value': 'all'}] + 
                [{'label': cat, 'value': cat} for cat in df['categoria'].unique()],
        value='all',
        clearable=False
    )

def create_region_filter(df):
    """Cria o filtro de região."""
    return dcc.Dropdown(
        id='region-filter',
        options=[{'label': 'Todas', 'value': 'all'}] + 
                [{'label': reg, 'value': reg} for reg in df['regiao'].unique()],
        value='all',
        clearable=False
    )
