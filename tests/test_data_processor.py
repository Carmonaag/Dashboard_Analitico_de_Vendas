
import pandas as pd
from utils.data_processor import load_data, process_data

def test_load_data():
    """Testa o carregamento de dados."""
    df = load_data('data/sales_data.csv')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_process_data():
    """Testa o processamento de dados."""
    df = load_data('data/sales_data.csv')
    df = process_data(df)
    assert 'mes' in df.columns
    assert 'ano' in df.columns
