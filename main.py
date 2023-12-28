from transform_data import filter_corrupted_data, merge_and_clean
from ships import load_ship_infos
from ports import *
from ships_in_ports import find_ships_in_ports_and_save
import pickle
import os

cache_file_path = 'ship_infos_cache.pkl'

#filter_corrupted_data(r"C:\Users\pdgni\Desktop\Statki\in", r"C:\Users\pdgni\Desktop\Statki\filtered", ';', 'utf_8_sig')

ship_infos = []
if os.path.exists(cache_file_path):
    with open(cache_file_path, 'rb') as file:
        ship_infos = pickle.load(file)
else:
    data = merge_and_clean(r"C:\Users\pdgni\Desktop\Statki\filtered", ';', 'utf_8_sig')
    ship_infos = load_ship_infos(data)
    with open(cache_file_path, 'wb') as file:
        pickle.dump(ship_infos, file)

ports = load_ports(r"C:\Users\pdgni\Desktop\Statki\ports_input.json")
find_ships_in_ports_and_save(ship_infos, ports, r"C:\Users\pdgni\Desktop\Statki\out")