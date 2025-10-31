
import redis
import pandas as pd
import json
import hashlib
from config import settings

# Inicializa a conexão com o Redis a partir da URL nas configurações
try:
    redis_client = redis.from_url(settings.REDIS_URL)
    redis_client.ping()
    print("Conexão com o Redis estabelecida com sucesso.")
except redis.exceptions.ConnectionError as e:
    print(f"Não foi possível conectar ao Redis: {e}")
    redis_client = None

def get_cache_key(filters):
    """Cria uma chave de cache única a partir dos filtros."""
    # Serializa os filtros de forma consistente
    serialized_filters = json.dumps(filters, sort_keys=True).encode('utf-8')
    # Retorna o hash SHA256 como chave
    return hashlib.sha256(serialized_filters).hexdigest()

def get_from_cache(key):
    """Busca dados do cache Redis."""
    if redis_client is None:
        return None
        
    cached_data = redis_client.get(key)
    if cached_data:
        print(f"Cache HIT para a chave: {key}")
        # Desserializa os dados de JSON para DataFrame
        return pd.read_json(json.loads(cached_data), orient='split')
    
    print(f"Cache MISS para a chave: {key}")
    return None

def set_to_cache(key, df, expiration_time=3600):
    """
    Armazena um DataFrame no cache Redis.
    O DataFrame é primeiro convertido para JSON.
    """
    if redis_client is None:
        return

    try:
        # Converte o DataFrame para JSON e depois para uma string para armazenar
        data_to_cache = df.to_json(date_format='iso', orient='split')
        redis_client.setex(key, expiration_time, json.dumps(data_to_cache))
        print(f"Dados armazenados no cache com a chave: {key}")
    except Exception as e:
        print(f"Erro ao armazenar dados no cache: {e}")

