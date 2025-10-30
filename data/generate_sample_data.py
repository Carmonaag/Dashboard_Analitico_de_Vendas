import pandas as pd
import numpy as np

def generate_data(n_records=500000):
    """Gera dados sintéticos de vendas."""
    np.random.seed(42)
    dates = pd.to_datetime(pd.date_range(start='2022-01-01', periods=n_records, freq='h'))
    
    df = pd.DataFrame({
        'data': dates,
        'valor': np.random.exponential(scale=100, size=n_records) + 50,
        'quantidade': np.random.poisson(lam=5, size=n_records) + 1,
        'categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Alimentos', 'Livros', 'Móveis', 'Esportes', 'Brinquedos', 'Automotivo'], n_records),
        'regiao': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste', 'Centro', 'Nordeste', 'Sudeste'], n_records),
        'produto': np.random.choice([f'Produto {i}' for i in range(1, 101)], n_records)
    })
    
    df['receita'] = df['valor'] * df['quantidade']
    df['mes'] = df['data'].dt.to_period('M').astype(str)
    df['ano'] = df['data'].dt.year
    
    return df

if __name__ == '__main__':
    df = generate_data()
    df.to_csv('data/sales_data.csv', index=False)
    print(f"{len(df)} registros foram gerados e salvos em 'data/sales_data.csv'")
