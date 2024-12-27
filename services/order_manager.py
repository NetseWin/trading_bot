from services.binance_api import BinanceAPI
from utils.logger import main_logger

class OrderManager:
    def __init__(self):
        self.api = BinanceAPI()

    def place_market_order(self, symbol, side, quantity):
        """Coloca una orden de mercado."""
        try:
            response = self.api.place_order(symbol, side, quantity)
            main_logger.info(f"Orden de mercado ejecutada: {response}")
            return response
        except Exception as e:
            main_logger.error(f"Error al colocar orden de mercado: {e}")
            return None

    def place_limit_order(self, symbol, side, quantity, price):
        """Coloca una orden límite."""
        try:
            response = self.api.client.order_limit(
                symbol=symbol, side=side, quantity=quantity, price=str(price)
            )
            main_logger.info(f"Orden límite colocada: {response}")
            return response
        except Exception as e:
            main_logger.error(f"Error al colocar orden límite: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """Cancela una orden pendiente."""
        try:
            response = self.api.client.cancel_order(symbol=symbol, orderId=order_id)
            main_logger.info(f"Orden cancelada: {response}")
            return response
        except Exception as e:
            main_logger.error(f"Error al cancelar orden: {e}")
            return None

    def place_stop_loss_take_profit_order(self, symbol, quantity, stop_price, take_price):
        """Combina órdenes de stop-loss y take-profit."""
        try:
            # Coloca orden stop-loss
            stop_order = self.api.client.create_order(
                symbol=symbol,
                side='SELL',
                type='STOP_LOSS_LIMIT',
                quantity=quantity,
                price=str(stop_price),
                stopPrice=str(stop_price)
            )
            main_logger.info(f"Orden stop-loss colocada: {stop_order}")

            # Coloca orden take-profit
            take_order = self.api.client.create_order(
                symbol=symbol,
                side='SELL',
                type='LIMIT',
                quantity=quantity,
                price=str(take_price)
            )
            main_logger.info(f"Orden take-profit colocada: {take_order}")

        except Exception as e:
            main_logger.error(f"Error al colocar órdenes stop-loss/take-profit: {e}")

    def check_balance(self, symbol, quantity, price, fee_rate=0.001):
        """
        Verifica si hay suficiente saldo para realizar una operación.
        Args:
            symbol (str): Par de trading (e.g., 'ETHUSDT').
            quantity (float): Cantidad de la operación.
            price (float): Precio actual del par.
            fee_rate (float): Comisión aplicada a la operación (por defecto, 0.1%).
        Returns:
            bool: True si el saldo es suficiente, False en caso contrario.
        """
        base_currency = symbol[-4:]  # Supone que el par termina en 'USDT'
        total_cost = quantity * price * (1 + fee_rate)  # Incluye la comisión
        balances = self.api.get_account_balance()
        available_balance = balances.get(base_currency, 0)  # Saldo disponible en USDT
        main_logger.info(f"Saldo disponible en {base_currency}: {available_balance:.2f}, Costo total estimado: {total_cost:.2f}")
        return available_balance >= total_cost

