import pandas as pd
from utils.logger import main_logger

def initial_market_analysis(api, symbol, interval):
    """Realiza un análisis inicial del mercado antes de comenzar a operar."""
    try:
        candles = api.client.get_klines(symbol=symbol, interval=interval, limit=100)
        df = pd.DataFrame(candles, columns=['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
                                            'CloseTime', 'QuoteAssetVolume', 'Trades',
                                            'TBBAV', 'TBQAV', 'Ignore'])
        df['Close'] = df['Close'].astype(float)
        main_logger.info("Análisis inicial del mercado completado.")
        return df
    except Exception as e:
        main_logger.error(f"Error al obtener datos iniciales del mercado: {e}")
        return None
