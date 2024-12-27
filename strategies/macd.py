import pandas as pd

def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    """Calcula el MACD, la Línea de Señal y el Histograma."""
    data['EMA_Short'] = data['Close'].ewm(span=short_window, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = data['EMA_Short'] - data['EMA_Long']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    return data

def macd_strategy(data):
    """Genera señales basadas en el MACD."""
    data = calculate_macd(data)
    data['Buy_Signal'] = (data['MACD'] > data['Signal_Line']) & (data['MACD_Histogram'] > 0)
    data['Sell_Signal'] = (data['MACD'] < data['Signal_Line']) & (data['MACD_Histogram'] < 0)
    return data
