import csv
from datetime import datetime

def log_simulated_trade(symbol, price, action, quantity, filename='simulated_trades.csv', fee_rate=0.001):
    """
    Registra una operación simulada en un archivo CSV.
    
    Args:
        symbol (str): Par de trading (e.g., 'ETHUSDT').
        price (float): Precio de la operación.
        action (str): Tipo de operación ('BUY' o 'SELL').
        quantity (float): Cantidad de la operación.
        filename (str): Nombre del archivo CSV donde se guarda la operación.
        fee_rate (float): Comisión aplicada a la operación (por defecto, 0.1%).
    """
    fee = price * quantity * fee_rate  # Calcula la comisión
    net_cost = price * quantity - fee if action == 'BUY' else price * quantity + fee  # Calcula el costo neto
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Escribe el encabezado si el archivo está vacío
            writer.writerow(['Fecha', 'Símbolo', 'Acción', 'Precio', 'Cantidad', 'Comisión', 'Costo Neto'])
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), symbol, action, price, quantity, fee, net_cost])
