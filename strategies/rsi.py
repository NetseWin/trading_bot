import pandas as pd

def calculate_rsi(data, window=14):
    """Calcula el Índice de Fuerza Relativa (RSI)"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))

    return data

def rsi_strategy(data, window=14):
    """Estrategia basada en el RSI"""
    data = calculate_rsi(data, window)

    # Genera señales de compra y venta
    data['Buy_Signal'] = data['RSI'] < 30  # Compra si RSI < 30
    data['Sell_Signal'] = data['RSI'] > 70  # Venta si RSI > 70

    return data

# Bloque de prueba
if __name__ == "__main__":
    # Datos de ejemplo
    data = {
        "Close": [100, 102, 101, 103, 104, 102, 101, 105, 106, 107, 108, 110, 109, 108, 107, 106, 105]
    }
    df = pd.DataFrame(data)

    # Aplica la estrategia RSI
    result = rsi_strategy(df, window=5)

    # Muestra las columnas relevantes
    print(result[['Close', 'RSI', 'Buy_Signal', 'Sell_Signal']])

    # Guarda los resultados en un archivo CSV
    result.to_csv('rsi_results.csv', index=False)
    print("Resultados guardados en 'rsi_results.csv'")
