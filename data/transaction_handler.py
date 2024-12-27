import csv
import time
from utils.logger import main_logger

def record_transaction(transaction_type, symbol, quantity, price, total, order_id):
    """Registra una transacción en un archivo CSV."""
    file_name = "transaction_history.csv"
    fields = ['type', 'symbol', 'quantity', 'price', 'total', 'order_id', 'timestamp']

    try:
        # Verificar si el archivo existe, si no, crearlo con encabezados
        try:
            with open(file_name, 'x', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
        except FileExistsError:
            pass

        # Registrar la transacción
        with open(file_name, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writerow({
                'type': transaction_type,
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'total': total,
                'order_id': order_id,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            })
    except Exception as e:
        main_logger.error(f"Error al registrar transacción: {e}")

def calculate_profit(symbol, quantity_sold, sell_price):
    """Calcula la ganancia/pérdida neta para una venta basada en el historial de transacciones."""
    file_name = "transaction_history.csv"
    try:
        with open(file_name, 'r') as f:
            reader = csv.DictReader(f)
            purchases = [row for row in reader if row['type'] == 'BUY' and row['symbol'] == symbol]

        # Calcular el costo promedio de la cantidad vendida
        remaining_quantity = quantity_sold
        total_cost = 0

        for purchase in purchases:
            purchase_qty = float(purchase['quantity'])
            purchase_price = float(purchase['price'])

            if remaining_quantity <= 0:
                break

            if purchase_qty <= remaining_quantity:
                total_cost += purchase_qty * purchase_price
                remaining_quantity -= purchase_qty
            else:
                total_cost += remaining_quantity * purchase_price
                remaining_quantity = 0

        if remaining_quantity > 0:
            main_logger.warning("No hay suficientes compras registradas para calcular el costo promedio.")
            return None

        total_revenue = quantity_sold * sell_price
        profit = total_revenue - total_cost

        return profit

    except FileNotFoundError:
        main_logger.warning("Archivo de historial de transacciones no encontrado. No se puede calcular la ganancia.")
        return None
    except Exception as e:
        main_logger.error(f"Error al calcular ganancia: {e}")
        return None
