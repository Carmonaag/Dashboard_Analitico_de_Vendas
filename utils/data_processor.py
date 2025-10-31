
import pandas as pd

def load_data(file_path):
    """Carrega os dados de um arquivo CSV."""
    return pd.read_csv(file_path, parse_dates=['data'])

def process_data(df):
    """Processa os dados de vendas."""
    df['mes'] = df['data'].dt.to_period('M').astype(str)
    df['ano'] = df['data'].dt.year
    return df
