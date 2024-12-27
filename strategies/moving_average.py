import pandas as pd
import matplotlib.pyplot as plt

def moving_average_strategy(data, short_window=5, long_window=10):
    """Estrategia de trading basada en medias móviles."""
    data['SMA_Short'] = data['Close'].rolling(window=short_window).mean()
    data['SMA_Long'] = data['Close'].rolling(window=long_window).mean()
    data['Signal'] = data['SMA_Short'] > data['SMA_Long']  # Señal de compra
    data['Sell_Signal'] = data['SMA_Short'] < data['SMA_Long']  # Señal de venta
    return data

def plot_strategy(data):
    """Grafica los precios y las señales de compra/venta."""
    plt.figure(figsize=(12, 6))

    # Gráfica del precio de cierre y medias móviles
    plt.plot(data['Close'], label='Precio de Cierre', color='blue', alpha=0.6)
    plt.plot(data['SMA_Short'], label='SMA Corta', color='green', alpha=0.6)
    plt.plot(data['SMA_Long'], label='SMA Larga', color='red', alpha=0.6)

    # Señales de compra
    buy_signals = data[data['Signal']]
    plt.scatter(buy_signals.index, buy_signals['Close'], label='Compra', marker='^', color='green', alpha=1)

    # Señales de venta
    sell_signals = data[data['Sell_Signal']]
    plt.scatter(sell_signals.index, sell_signals['Close'], label='Venta', marker='v', color='red', alpha=1)

    plt.title('Estrategia de Medias Móviles')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid()

    # Guardar el gráfico como archivo PNG
    output_file = 'moving_average_plot.png'
    plt.savefig(output_file)
    print(f"Gráfico guardado como '{output_file}'")

# Bloque de pruebas
if __name__ == "__main__":
    # Datos de ejemplo para probar
    data = {
        "Close": [100, 102, 101, 103, 104, 102, 101, 105, 106, 107, 108]
    }
    df = pd.DataFrame(data)

    # Aplica la estrategia con ventanas específicas
    short_window = 3
    long_window = 5
    result = moving_average_strategy(df, short_window, long_window)

    # Muestra el DataFrame con las columnas SMA y Signal
    print(result[['Close', 'SMA_Short', 'SMA_Long', 'Signal', 'Sell_Signal']])

    # Guarda los resultados en un archivo CSV
    result.to_csv('moving_average_results.csv', index=False)
    print("Resultados guardados en 'moving_average_results.csv'")

    # Guarda el gráfico
    plot_strategy(result)

