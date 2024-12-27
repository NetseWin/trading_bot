import logging
import os

def setup_logger(name, log_file, level=logging.INFO):
    """Crea y configura un logger."""
    # Verifica que el directorio exista; si no, lo crea
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Logger principal
main_logger = setup_logger('main_logger', 'logs/trading_bot.log')

# Bloque para pruebas
if __name__ == "__main__":
    main_logger.info("Esto es un mensaje de prueba INFO.")
    main_logger.warning("Esto es un mensaje de prueba WARNING.")
    main_logger.error("Esto es un mensaje de prueba ERROR.")
