from dataclasses import dataclass
from datetime import datetime
from collections import namedtuple
from typing import List, Tuple
import re
import sys

@dataclass
class HistoricalRecord:
    time: datetime
    position: Tuple[float, float]
    speed: float


@dataclass
class ShipInfo:
    MMSI: int
    Vessel_Name: str
    Length: float
    Type: int
    History: List[HistoricalRecord]

def load_ship_infos(df):
    # Extract unique MMSI values
    unique_mmsi_values = df['~MMSI'].unique()

    # Create a dictionary to store DataFrames for each MMSI
    ship_infos = []

    # Iterate over unique MMSI values
    for mmsi in unique_mmsi_values:
        # Filter rows for the current MMSI
        mmsi_df = df[df['~MMSI'] == mmsi]
        ship_infos.append(create_ship_info(mmsi_df))

    return ship_infos

def convert_coordinates(coord_str):
    # Replace commas with periods and convert coordinates from string format to float
    degrees, minutes_str = re.findall(r'(\d+)° (\d+,\d+)', coord_str)[0]
    minutes = float(minutes_str.replace(',', '.'))
    return float(degrees) + minutes / 60.0

def convert_speed(speed_str):
    # Handle '0,0' case by returning 0.0
    if speed_str == '0,0':
        return 0.0
    else:
        return float(speed_str.replace(',', '.'))

def create_ship_info(dataframe):
    # Extracting information from the DataFrame
    try:
        mmsi = int(dataframe['~MMSI'].iloc[0])
    except:
        return None

    vessel_name = dataframe['Vessel Name'].iloc[0]
    
    # Checking if 'Length' and 'Ship Type' are always NaN
    length_is_nan = dataframe['Length'].isna().all()
    ship_type_is_nan = dataframe['Ship Type'].isna().all()

    # If 'Length' and 'Ship Type' are always NaN, return None
    if length_is_nan and ship_type_is_nan:
        return None

    # If 'Length' and 'Ship Type' are not always NaN, extract their values from the first non-NaN record
    length = float('nan')
    ship_type = float('nan')

    non_nan_length_records = dataframe['Length'].dropna()
    non_nan_ship_type_records = dataframe['Ship Type'].dropna()

    if not non_nan_length_records.empty:
        length = float(non_nan_length_records.iloc[0])

    if not non_nan_ship_type_records.empty:
        ship_type = int(non_nan_ship_type_records.iloc[0])

    # Creating HistoricalRecord objects
    history = []
    for index, row in dataframe.iterrows():
        time = datetime.strptime(row['Received Time UTC'], "%d-%m-%Y %H:%M:%S")
        latitude = convert_coordinates(row['Latitude'])
        longitude = convert_coordinates(row['Longitude'])
        position = (latitude, longitude)
        speed = convert_speed(row['Speed Over Ground (SOG)'])
        historical_record = HistoricalRecord(time=time, position=position, speed=speed)
        history.append(historical_record)

    # Creating ShipInfo object
    ship_info = ShipInfo(MMSI=mmsi, Vessel_Name=vessel_name, Length=length, Type=ship_type, History=history)

    return ship_info