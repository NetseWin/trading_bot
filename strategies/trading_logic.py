class TradingLogic:
    @staticmethod
    def calculate_operable_quantity(balance, price, fee_rate=0.001, precision=4, min_notional=10, percentage=0.7):
        """
        Calcula la cantidad máxima operable basada en el saldo disponible y el filtro de notional.
        
        Args:
            balance (float): Saldo disponible en la cuenta.
            price (float): Precio actual del activo.
            fee_rate (float, opcional): Comisión de la operación. Default: 0.001 (0.1%).
            precision (int, opcional): Precisión decimal para redondeo. Default: 4.
            min_notional (float, opcional): Valor mínimo permitido por operación. Default: 10.
            percentage (float, opcional): Porcentaje del saldo a utilizar. Default: 0.7 (70%).
        
        Returns:
            float: Cantidad máxima operable, redondeada según la precisión.
        """
        max_quantity = (balance * percentage) / (price * (1 + fee_rate))
        if max_quantity * price < min_notional:
            return 0
        return round(max_quantity, precision)

    @staticmethod
    def meets_expected_margin(buy_price, sell_price, fee_rate=0.001, min_margin=0.003):
        """
        Evalúa si la diferencia de precios entre compra y venta cumple con el margen esperado.
        
        Args:
            buy_price (float): Precio de compra.
            sell_price (float): Precio de venta.
            fee_rate (float, opcional): Comisión de la operación. Default: 0.001 (0.1%).
            min_margin (float, opcional): Margen mínimo esperado. Default: 0.003 (0.3%).
        
        Returns:
            bool: True si el margen esperado es mayor al mínimo requerido, False en caso contrario.
        """
        net_gain = (sell_price - buy_price) / buy_price
        return net_gain > (min_margin + 2 * fee_rate)

    @staticmethod
    def should_buy(latest_price, lower_band, rsi, min_rsi=35):
        """
        Determina si es un buen momento para comprar.
        
        Args:
            latest_price (float): Precio más reciente del activo.
            lower_band (float): Valor de la banda inferior de Bollinger.
            rsi (float): Valor actual del RSI.
            min_rsi (int, opcional): Umbral mínimo del RSI para considerar una compra. Default: 35.
        
        Returns:
            bool: True si las condiciones de compra se cumplen, False en caso contrario.
        """
        return latest_price < lower_band and rsi < min_rsi

    @staticmethod
    def should_sell(latest_price, cost_avg, upper_band, macd, signal_line, fee_rate=0.001, min_margin=0.003, max_rsi=75):
        """
        Determina si es un buen momento para vender.
        
        Args:
            latest_price (float): Precio más reciente del activo.
            cost_avg (float): Costo promedio del activo.
            upper_band (float): Valor de la banda superior de Bollinger.
            macd (float): Valor actual del MACD.
            signal_line (float): Valor actual de la línea de señal del MACD.
            fee_rate (float, opcional): Comisión de la operación. Default: 0.001 (0.1%).
            min_margin (float, opcional): Margen mínimo esperado. Default: 0.003 (0.3%).
            max_rsi (int, opcional): Umbral máximo del RSI para considerar una venta. Default: 75.
        
        Returns:
            bool: True si las condiciones de venta se cumplen, False en caso contrario.
        """
        expected_margin = (latest_price - cost_avg) / cost_avg
        return (
            latest_price > cost_avg * (1 + fee_rate + min_margin) and
            latest_price > upper_band and
            macd > signal_line and
            expected_margin > (min_margin + 2 * fee_rate)
        )

