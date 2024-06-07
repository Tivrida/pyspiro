import numpy as np
import xarray as xr
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Robinson1987:
    def __init__(self):
        pass  # Убрана папка для результатов

    def _check_dimensions(self, *datasets):
        # Проверяем размеры по трем координатам: ae_bin, lat, mlt
        try:
            dims = ['ae_bin', 'lat', 'mlt']
            for dim in dims:
                sizes = [ds.sizes.get(dim, None) for ds in datasets]
                if not all(size == sizes[0] for size in sizes if size is not None):
                    logging.error(f'The dimensions along the {dim} coordinate do not match:{sizes}')
                    raise ValueError(f'Dimensions at coordinate {dim} do not match')
        except Exception as e:
            logging.error(f"Error checking dimensions: {e}")
            raise  # Переброска исключения

    def pedersen_conductivity(self, E_o_path, Phi_path):
        try:
            E_o_data = xr.open_dataset(E_o_path)
            Phi_data = xr.open_dataset(Phi_path)

            # Проверяем размеры датасетов
            self._check_dimensions(E_o_data, Phi_data)

            # Используем правильные переменные
            E_o = E_o_data['Energy']
            Phi = Phi_data['flux']

            result = (40 * E_o / (16 + E_o ** 2)) * np.sqrt(Phi)
            logging.info(f'Pedersen conductivity result:\n{result}')

            result_dataset = xr.Dataset({'pedersen_conductivity': result})
            result_dataset.attrs = {
                'units :': 'Pedersen conductivity',
                'standard_name': 'Pedersen conductivity,  Spiro1982 model',
                'description': 'Spiro 1982 model, provided as tabulated values. Used to interpolate the average accelerating electron energy flux contours for the four AE levels used in this model',
                'SPIRO1982_reference': 'https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JA087ia10p08215',
                'ae_bin_long_name': 'Auroral electrojet, [nT.]',
                'lat_long_name': 'latitude, [deg.]',
                'mlt_long_name': 'magnetic local time, [hours.]',
            }
            print(result)
        except Exception as e:
            logging.error(f"Error when calculating Pedersen conductivity: {e}")
            raise  # Переброска исключения

    def hall_conductivity(self, E_o_path, Ped_path):
        try:
            E_o_data = xr.open_dataset(E_o_path)
            Ped_data = xr.open_dataset(Ped_path)

            # Проверяем размеры датасетов
            self._check_dimensions(E_o_data, Ped_data)

            # Используем правильные переменные
            E_o = E_o_data['Energy']
            Ped = Ped_data['Pedersen']

            result = 0.45*Ped*(E_o)**0.85

            logging.info(f'Result of Hall conductivity:\n{result}')

            result_dataset = xr.Dataset({'hall_conductivity': result})
            result_dataset.attrs = {
                'units :': 'Hall conductivity',
                'standard_name': 'Hall conductivity,  Spiro1982 model',
                'description': 'Spiro 1982 model, provided as tabulated values. Used to interpolate the average accelerating electron energy flux contours for the four AE levels used in this model',
                'SPIRO1982_reference': 'https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JA087ia10p08215',
                'ae_bin_long_name': 'Auroral electrojet, [nT.]',
                'lat_long_name': 'latitude, [deg.]',
                'mlt_long_name': 'magnetic local time, [hours.]',
            }
            print(result)
        except Exception as e:
            logging.error(f"Error when calculating Hall conductivity: {e}")
            raise  # Переброска исключения

    def process_dataset(self, dataset_path, operation, **kwargs):
        try:
            dataset = xr.open_dataset(dataset_path)

            # Проверка параметров
            if 'ae_bin' in kwargs and not isinstance(kwargs['ae_bin'], int):
                logging.error('The format of the ae_bin parameter is incorrect, an integer is required')
                raise ValueError('ae_bin must be an integer')

            if 'lat' in kwargs and not isinstance(kwargs['lat'], int):
                logging.error('Invalid lat parameter format, integer required')
                raise ValueError('lat must be an integer')

            if 'mlt' in kwargs and kwargs['mlt'] not in (np.arange(0, 24) + 0.5).tolist():
                logging.error('The format of the mlt parameter is incorrect, the value from np.arange(0, 24) + 0.5 is required')
                raise ValueError('mlt must be the value from np.arange(0, 24) + 0.5')

            logging.error(f'Invalid operation: {operation}')
            raise ValueError('Invalid operation. Use interp or sel.')
        except Exception as e:
            logging.error(f"Error while processing the dataset: {e}")
            raise  # Переброска исключения






