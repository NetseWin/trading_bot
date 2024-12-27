import pandas as pd
import matplotlib.pyplot as plt

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    """
    Calcula las Bandas de Bollinger.
    - window: Número de períodos para la SMA y la desviación estándar.
    - num_std_dev: Número de desviaciones estándar para las bandas superior e inferior.
    """
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data['Upper_Band'] = data['SMA'] + (num_std_dev * data['Close'].rolling(window=window).std())
    data['Lower_Band'] = data['SMA'] - (num_std_dev * data['Close'].rolling(window=window).std())
    return data

def bollinger_strategy(data, window=20, num_std_dev=2):
    """
    Estrategia basada en Bandas de Bollinger.
    - Compra cuando el precio está por debajo de la banda inferior.
    - Venta cuando el precio está por encima de la banda superior.
    """
    data = calculate_bollinger_bands(data, window, num_std_dev)
    data['Buy_Signal'] = data['Close'] < data['Lower_Band']
    data['Sell_Signal'] = data['Close'] > data['Upper_Band']
    return data

def plot_bollinger_bands(data):
    """
    Grafica las Bandas de Bollinger junto con los precios.
    """
    plt.figure(figsize=(12, 6))

    # Gráfica del precio de cierre
    plt.plot(data['Close'], label='Precio de Cierre', color='blue', alpha=0.6)

    # Gráfica de las bandas
    plt.plot(data['SMA'], label='SMA (Media Móvil)', color='orange', alpha=0.8)
    plt.plot(data['Upper_Band'], label='Banda Superior', color='red', linestyle='--', alpha=0.8)
    plt.plot(data['Lower_Band'], label='Banda Inferior', color='green', linestyle='--', alpha=0.8)

    # Señales de compra y venta
    buy_signals = data[data['Buy_Signal']]
    plt.scatter(buy_signals.index, buy_signals['Close'], label='Compra', marker='^', color='green', alpha=1)

    sell_signals = data[data['Sell_Signal']]
    plt.scatter(sell_signals.index, sell_signals['Close'], label='Venta', marker='v', color='red', alpha=1)

    plt.title('Bandas de Bollinger')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Guardar gráfico como archivo PNG
    plt.savefig('bollinger_bands_plot.png')
    print("Gráfico guardado como 'bollinger_bands_plot.png'")

# Bloque de prueba
if __name__ == "__main__":
    # Datos de ejemplo para probar
    data = {
        "Close": [100, 102, 101, 103, 104, 102, 101, 105, 106, 107, 108, 110, 111, 109, 107, 106, 105, 104, 102, 101]
    }
    df = pd.DataFrame(data)

    # Aplica la estrategia de Bandas de Bollinger
    result = bollinger_strategy(df, window=5, num_std_dev=2)

    # Muestra las columnas relevantes
    print(result[['Close', 'SMA', 'Upper_Band', 'Lower_Band', 'Buy_Signal', 'Sell_Signal']])

    # Guarda los resultados en un archivo CSV
    result.to_csv('bollinger_bands_results.csv', index=False)
    print("Resultados guardados en 'bollinger_bands_results.csv'")

    # Grafica las Bandas de Bollinger
    plot_bollinger_bands(result)
