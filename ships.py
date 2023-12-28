from dataclasses import dataclass
from datetime import datetime
from collections import namedtuple
from typing import List, Tuple
import re
import sys
import pandas as pd

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
    #df = df.dropna(subset=['Vessel Name'])
    df['Vessel Name'] = df['Vessel Name'].str.strip()

    unique_mmsi_values = df['~MMSI'].unique()

    # Create a dictionary to store DataFrames for each MMSI
    ship_infos = []

    print(f"Number of ships: {len(unique_mmsi_values)}")

    # Iterate over unique MMSI values
    for mmsi in unique_mmsi_values:
        # Filter rows for the current MMSI
        mmsi_df = df[df['~MMSI'] == mmsi]
        try:
            ship_infos.append(create_ship_info(mmsi_df))
        except Exception as e:
            print(f"An error occurred during transformation of {mmsi}: {e}")

    return ship_infos

def convert_coordinates(coord_str):
    # Replace commas with periods and convert coordinates from string format to float
    degrees, minutes_str = re.findall(r'(\d+)° (\d+,\d+)', coord_str)[0]
    minutes = float(minutes_str.replace(',', '.'))
    return float(degrees) + minutes / 60.0

def convert_speed(speed):
    if speed is float:
        return speed
    else:
        if speed == '0,0':
            return 0.0
        else:
            return float(speed.replace(',', '.'))

def create_ship_info(dataframe):
    # Extracting information from the DataFrame
    try:
        mmsi = int(dataframe['~MMSI'].iloc[0])
    except:
        return None

    vessel_name = dataframe['Vessel Name'].iloc[0]

    print(f"Creating info about {vessel_name} ship.\n")

    # If 'Length' and 'Ship Type' are not always NaN, extract their values from the first non-NaN record
    length = float('nan')
    ship_type = float('nan')

    non_nan_length_records = dataframe['Length'].dropna()
    non_nan_ship_type_records = dataframe['Ship Type'].dropna()

    if not non_nan_length_records.empty:
        length = float(non_nan_length_records.iloc[0])
    else:
        length = "Unknown"

    if not non_nan_ship_type_records.empty:
        ship_type = int(non_nan_ship_type_records.iloc[0])
    else:
        ship_type = "Unknown"
        
    # Convert 'Received Time UTC' to datetime format
    dataframe.loc[:, 'Received Time UTC'] = pd.to_datetime(dataframe['Received Time UTC'], format="%d-%m-%Y %H:%M:%S")

    # Sort the DataFrame by 'Received Time UTC'
    dataframe = dataframe.sort_values(by='Received Time UTC')
    
    history = []
    prev = None
    for index, row in dataframe.iterrows():
        time = row['Received Time UTC'].to_pydatetime()
        if prev is not None:
            if(time < prev):
                print(f"Time of ship {vessel_name}: time:{str(time)} prev:{str(prev)}")
        latitude = convert_coordinates(row['Latitude'])
        longitude = convert_coordinates(row['Longitude'])
        position = (latitude, longitude)
        speed = convert_speed(row['Speed Over Ground (SOG)'])
        historical_record = HistoricalRecord(time=time, position=position, speed=speed)
        history.append(historical_record)
        prev = time

    # Creating ShipInfo object
    ship_info = ShipInfo(MMSI=mmsi, Vessel_Name=vessel_name, Length=length, Type=ship_type, History=history)

    return ship_info