import functools
import xarray as xr
from importlib_resources import files
import logging

# Настройка конфигурации логирования
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Глобальный кэш для файлов
file_cache = {}

@functools.lru_cache(maxsize=4)
def load_file(file_name):
    logging.debug(f"Attempting to load file: {file_name}")
    try:
        file_path = files("pyspiro._data").joinpath(file_name)
        if not file_path.exists():
            error_msg = f"File not found: {file_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

        logging.debug(f"Loading dataset from: {file_path}")
        data = xr.load_dataset(str(file_path))
        logging.info(f"Successfully loaded file: {file_name}")
        return data
    except Exception as e:
        logging.exception(f"Error occurred while getting {file_name}")
        raise  # Переброска исключения для обработки выше по стеку вызовов

def get_characteristic():
    logging.debug("Requesting characteristic data")
    try:
        return load_file("characteristic_data.nc").copy()
    except Exception as e:
        logging.error(f"Failed to retrieve characteristic data: {e}")
        raise  # Переброска исключения

def get_energy_flux():
    logging.debug("Requesting energy flux data")
    try:
        return load_file("flux_data.nc").copy()
    except Exception as e:
        logging.error(f"Failed to retrieve energy flux data: {e}")
        raise  # Переброска исключения

def get_hall():
    logging.debug("Requesting hall data")
    try:
        return load_file("hall_data.nc").copy()
    except Exception as e:
        logging.error(f"Failed to retrieve hall data: {e}")
        raise  # Переброска исключения

def get_pedersen():
    logging.debug("Requesting pedersen data")
    try:
        return load_file("pedersen_data.nc").copy()
    except Exception as e:
        logging.error(f"Failed to retrieve pedersen data: {e}")
        raise  # Переброска исключения


