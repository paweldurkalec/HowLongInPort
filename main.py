from transform_data import filter_corrupted_data, merge_and_clean
from ships import load_ship_infos
from ports import *

#filter_corrupted_data(r"C:\Users\pdgni\Desktop\Statki\in", r"C:\Users\pdgni\Desktop\Statki\filtered", ';', 'utf_8_sig')
#ports = load_ports(r"C:\Users\pdgni\Desktop\Statki\ports_input.json")

data = merge_and_clean(r"C:\Users\pdgni\Desktop\Statki\filtered", ';', 'utf_8_sig')

#data.to_csv(r"C:\Users\pdgni\Desktop\Statki\temp.csv", sep=";", encoding='utf_8_sig', index=False)

ship_infos = load_ship_infos(data)

print(ship_infos[0])


