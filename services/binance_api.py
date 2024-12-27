from binance.client import Client
from utils.config import API_KEY, SECRET_KEY

class BinanceAPI:
    def __init__(self):
        self.client = Client(API_KEY, SECRET_KEY)

    def get_account_balance(self):
        """Consulta los balances disponibles en la cuenta."""
        account = self.client.get_account()
        balances = account['balances']
        return {b['asset']: float(b['free']) for b in balances if float(b['free']) > 0}

    def get_price(self, symbol):
        """Obtiene el precio actual de un par."""
        ticker = self.client.get_ticker(symbol=symbol)
        return float(ticker['lastPrice'])

    def place_order(self, symbol, side, quantity):
        """Coloca una orden de mercado."""
        return self.client.order_market(
            symbol=symbol,
            side=side,
            quantity=quantity
        )
