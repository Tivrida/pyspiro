import numpy as np
import xarray as xr
import logging

from pyspiro._load_file import get_characteristic
from pyspiro._load_file import get_energy_flux
from pyspiro._load_file import get_hall
from pyspiro._load_file import get_pedersen

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class Spiro1982:
    def __init__(self):
        self.datasets = {}

    def load_datasets(self):
        logging.info("Loading datasets...")
        try:
            self.datasets['characteristic_data'] = get_characteristic()
            self.datasets['flux_data'] = get_energy_flux()
            self.datasets['hall_data'] = get_hall()
            self.datasets['pedersen_data'] = get_pedersen()
            logging.info("Datasets have been successfully loaded.")
        except Exception as e:
            logging.error(f"Error loading datasets: {e}")
            raise  # Переброска исключения

    def show_dataset(self, dataset_name):
        try:
            if (dataset := self.datasets.get(dataset_name)) is not None:
                print("Dataset data:")
                print(dataset.to_array().values)
                print("\nDataset metadata:")
                for key, value in dataset.attrs.items():
                    print(f"{key}: {value}")
            else:
                logging.error("Dataset not found. Please load the datasets first.")
                raise KeyError(f"Dataset {dataset_name} not found.")
        except Exception as e:
            logging.error(f"Error when displaying dataset {dataset_name}: {e}")
            raise  # Переброска исключения

    def _check_dimensions(self, *datasets):
        dims = ['ae_bin', 'lat', 'mlt']
        try:
            for dim in dims:
                sizes = [ds.sizes.get(dim, None) for ds in datasets]
                if not all(size == sizes[0] for size in sizes if size is not None):
                    logging.error(f'The dimensions along the {dim} coordinate do not match: {sizes}')
                    raise ValueError(f'Dimensions at coordinate {dim} do not match')
        except Exception as e:
            logging.error(f"Error checking dimensions: {e}")
            raise  # Переброска исключения

    def execute_operation(self, dataset_name, operation, **kwargs):
        dataset = self.datasets.get(dataset_name)
        if dataset is None:
            logging.error(f"Dataset {dataset_name} not found.")
            raise KeyError(f"Dataset {dataset_name} not found.")

        try:
            if operation == 'interp':
                new_ae_bin = np.linspace(dataset.ae_bin.min(), dataset.ae_bin.max(), len(dataset.ae_bin) * 2)
                new_lat = np.linspace(dataset.lat.min(), dataset.lat.max(), len(dataset.lat) * 2)
                new_mlt = np.linspace(dataset.mlt.min(), dataset.mlt.max(), len(dataset.mlt) * 2)
                result = dataset.interp(ae_bin=new_ae_bin, lat=new_lat, mlt=new_mlt)

                array_result = result.to_array().values
                print(array_result)
            elif operation == 'sel':
                selectors = {k: kwargs[k] for k in ['ae_bin', 'lat', 'mlt'] if k in kwargs}
                result = dataset.sel(selectors)

                array_result = result.to_array().values
                print(array_result)
            else:
                logging.error("Invalid operation.")
                return
        except Exception as e:
            logging.error(f"Error during operation {operation}: {e}")
            raise  # Переброска исключения

    def power_calculation(self, AE_range):
        try:
            AE_values = np.arange(AE_range[0], AE_range[1] + 1)
            AE_mean = np.mean(AE_values)
            power_values = (1.75 * (AE_mean / 100) + 1.6) * 10 ** 10
            # Используем форматирование строки для вывода в научной нотации
            formatted_power_values = format(power_values, '.3e')
            print(formatted_power_values)
            logging.info("Power calculation completed successfully.")
            return formatted_power_values
        except Exception as e:
            logging.error(f"Error when calculating power: {e}")
            raise  # Переброска исключения

