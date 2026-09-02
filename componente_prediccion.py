import pandas as pd

def estimar_necesidad_riego(df: pd.DataFrame) -> float:
    #Calcularemos un estimado  de agua necesaria para mantener la humedad promedio
    
    if df.empty:
        return 0.0
    
    humedad_promedio = float(df['humedad_suelo_pct'].mean())
    
    if humedad_promedio < 40.0:
        litros_requeridos = (40.0 - humedad_promedio) * 150.0
        return float(litros_requeridos)
    
    return 0.0