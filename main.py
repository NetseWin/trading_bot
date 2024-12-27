from services.binance_api import BinanceAPI
from strategies.moving_average import moving_average_strategy
from strategies.rsi import rsi_strategy
from strategies.macd import macd_strategy
from strategies.bollinger_bands import bollinger_strategy
from strategies.trading_logic import TradingLogic
from services.order_manager import OrderManager
from services.market_analysis import initial_market_analysis
from data.transaction_handler import record_transaction, calculate_profit
import pandas as pd
import time
from utils.logger import main_logger

def main():
    symbol = "ETHUSDT"
    interval = "1m"  # Intervalo para datos históricos
    short_window = 5  # Ventana para SMA corta
    long_window = 10  # Ventana para SMA larga
    rsi_window = 14  # Ventana para RSI
    fee_rate = 0.001  # Tasa de comisión
    precision = 4  # Precisión para ETH/USDT
    min_notional = 10  # Valor mínimo notional
    percentage = 0.7  # Porcentaje del saldo a usar (actualizado a 0.7)
    min_margin = 0.003  # Margen mínimo esperado ajustado
    is_simulation = False  # Activar el modo simulado

    main_logger.info("Iniciando el bot de trading... (Simulación)" if is_simulation else "Iniciando el bot de trading...")

    api = BinanceAPI()
    order_manager = OrderManager()
    simulated_balance = {"USDT": 1000, "ETH": 0}  # Balance inicial para simulaciones

    market_data = initial_market_analysis(api, symbol, interval)
    if market_data is None:
        main_logger.error("No se pudo obtener datos del mercado. Finalizando el bot.")
        return

    while True:
        try:
            # Obtén datos históricos
            candles = api.client.get_klines(symbol=symbol, interval=interval, limit=100)
            df = pd.DataFrame(candles, columns=['OpenTime', 'Open', 'High', 'Low', 'Close', 'Volume',
                                                'CloseTime', 'QuoteAssetVolume', 'Trades',
                                                'TBBAV', 'TBQAV', 'Ignore'])
            df['Close'] = df['Close'].astype(float)

            # Aplica estrategias
            df = moving_average_strategy(df, short_window, long_window)
            df = rsi_strategy(df, rsi_window)
            df = macd_strategy(df)
            df = bollinger_strategy(df)

            # Datos recientes
            latest_price = df['Close'].iloc[-1]
            lower_band = df['Lower_Band'].iloc[-1]
            upper_band = df['Upper_Band'].iloc[-1]
            rsi = df['RSI'].iloc[-1]
            macd = df['MACD'].iloc[-1]
            signal_line = df['Signal_Line'].iloc[-1]

            # Registrar los datos técnicos más recientes
            main_logger.info(
                f"Último precio: {latest_price:.2f}, SMA_Corta: {df['SMA_Short'].iloc[-1]:.2f}, "
                f"SMA_Larga: {df['SMA_Long'].iloc[-1]:.2f}, RSI: {rsi:.2f}, MACD: {macd:.2f}, "
                f"Signal_Line: {signal_line:.2f}, Upper_Band: {upper_band:.2f}, Lower_Band: {lower_band:.2f}"
            )

            # Saldo (simulado o real)
            balances = simulated_balance if is_simulation else api.get_account_balance()
            usdt_balance = balances.get('USDT', 0)
            eth_balance = balances.get('ETH', 0)

            # Log de los saldos actuales
            main_logger.info(
                f"Saldo actual: USDT: {usdt_balance:.2f}, ETH: {eth_balance:.4f}"
            )

            if usdt_balance == 0 and eth_balance == 0:
                main_logger.warning("No hay saldo disponible para operar. Esperando próxima iteración.")
                time.sleep(60)
                continue

            # Cantidades dinámicas
            quantity_buy = TradingLogic.calculate_operable_quantity(
                usdt_balance, latest_price, fee_rate, precision, min_notional, percentage
            )
            quantity_sell = TradingLogic.calculate_operable_quantity(
                eth_balance * latest_price, latest_price, fee_rate, precision, min_notional, percentage
            )

            # Costo promedio
            cost_avg = None
            if eth_balance > 0:
                cost_avg = calculate_profit(symbol, eth_balance, latest_price) / eth_balance

            # Simulación de compra
            if TradingLogic.should_buy(latest_price, lower_band, rsi, min_rsi=35) and quantity_buy > 0:  # Ajuste en el umbral de RSI
                if is_simulation:
                    main_logger.info(f"🔔 ¡Simulación de COMPRA! {quantity_buy} ETH a {latest_price:.2f}")
                    simulated_balance["USDT"] -= quantity_buy * latest_price
                    simulated_balance["ETH"] += quantity_buy
                else:
                    main_logger.info(f"🔔 ¡Alerta de COMPRA detectada! {quantity_buy} ETH a {latest_price:.2f}")
                    response = order_manager.place_market_order(symbol, 'BUY', quantity_buy)
                    if response:
                        record_transaction('BUY', symbol, quantity_buy, latest_price, quantity_buy * latest_price, response['orderId'])

            # Simulación de venta
            elif cost_avg is not None and TradingLogic.should_sell(
                latest_price, cost_avg, upper_band, macd, signal_line, fee_rate, min_margin, max_rsi=75
            ) and quantity_sell > 0:
                if is_simulation:
                    main_logger.info(f"🔔 ¡Simulación de VENTA! {quantity_sell} ETH a {latest_price:.2f}")
                    simulated_balance["USDT"] += quantity_sell * latest_price
                    simulated_balance["ETH"] -= quantity_sell
                else:
                    main_logger.info(f"🔔 ¡Alerta de VENTA detectada! {quantity_sell} ETH a {latest_price:.2f}")
                    response = order_manager.place_market_order(symbol, 'SELL', quantity_sell)
                    if response:
                        record_transaction('SELL', symbol, quantity_sell, latest_price, quantity_sell * latest_price, response['orderId'])

            else:
                main_logger.info("Sin señales claras en este momento.")

            # Balance actual
            if is_simulation:
                main_logger.info(f"Saldo simulado: USDT: {simulated_balance['USDT']:.2f}, ETH: {simulated_balance['ETH']:.4f}")

            time.sleep(60)

        except Exception as e:
            main_logger.error(f"Error en el bot: {e}")
            time.sleep(10)  # Reintento tras error

if __name__ == "__main__":
    main()










