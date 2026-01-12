import duckdb
import pandas as pd
import numpy as np
import time

FILE_NAME = 'hopital_data.parquet'
NB_ROWS = 5_000_000 # On monte à 5M pour bien voir la différence

def setup_data():
    print(f"--- 1. Génération de {NB_ROWS} lignes ---")
    df = pd.DataFrame({
        'patient_id': np.arange(NB_ROWS),
        'age': np.random.randint(18, 95, NB_ROWS),
        'imc': np.random.uniform(15, 45, NB_ROWS),
        'service': np.random.choice(['Urgences', 'Cardio', 'Radiologie', 'Onco', 'Pédia'], NB_ROWS)
    })
    df.to_parquet(FILE_NAME)
    print(f"Fichier {FILE_NAME} créé.\n")

def benchmark_pandas():
    print("--- 2. Benchmark PANDAS (Chargement complet + Calcul) ---")
    start = time.time()
    # Pandas doit charger TOUT le fichier et TOUTES les colonnes en RAM
    df = pd.read_parquet(FILE_NAME)
    res = df[df['age'] > 50].groupby('service')['imc'].mean().sort_values(ascending=False)
    print(res)
    end = time.time()
    return end - start

def benchmark_duckdb():
    print("\n--- 3. Benchmark DUCKDB (Streaming + Colonnaire) ---")
    start = time.time()
    # DuckDB ne lit que les colonnes 'age', 'service' et 'imc' en streaming
    res = duckdb.sql(f"""
        SELECT service, round(avg(imc), 2) as imc_moyen
        FROM '{FILE_NAME}'
        WHERE age > 50
        GROUP BY service
        ORDER BY imc_moyen DESC
    """)
    res.show()
    end = time.time()
    return end - start

if __name__ == "__main__":
    setup_data()
    
    t_pd = benchmark_pandas()
    print(f"Temps Pandas : {t_pd:.4f} sec")
    
    t_db = benchmark_duckdb()
    print(f"Temps DuckDB : {t_db:.4f} sec")
    
    print(f"\n🚀 DuckDB est environ {round(t_pd/t_db, 1)}x plus rapide ici !")