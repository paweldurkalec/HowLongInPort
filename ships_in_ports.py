import pandas as pd
import os
from ports import is_inside

def strfdelta(tdelta, fmt="{hours}:{minutes}:{seconds}"):
    hours = tdelta.days * 24 + tdelta.seconds // 3600
    minutes, seconds = divmod(tdelta.seconds % 3600, 60)
    return fmt.format(hours=hours, minutes=minutes, seconds=seconds)

def find_ships_in_ports_and_save(ship_infos, ports, output_directory):
    result_data = []
    print(f"Calculating time in ports...\n")

    for ship_info in ship_infos:
        if ship_info is None:
            continue
        
        print(f"Calculating time in ports for {ship_info.Vessel_Name} ship.\n")

        for port in ports:
            in_port = False
            start_time = None
            total_time_in_port = pd.Timedelta(0)

            for record in ship_info.History:
                if is_inside(port.edges, *record.position) and record.speed == 0:
                    if not in_port:
                        in_port = True
                        start_time = record.time
                elif in_port:
                    in_port = False
                    end_time = record.time
                    time_span = end_time - start_time
                    total_time_in_port += time_span

            # Check if the ship is still inside the port with speed 0 when the historical data ends
            if in_port and ship_info.History[-1].speed == 0:
                end_time = ship_info.History[-1].time
                time_span = end_time - start_time
                total_time_in_port += time_span

            if total_time_in_port > pd.Timedelta(hours=2) and total_time_in_port < pd.Timedelta(hours=6*24):
                result_data.append({
                    'MMSI': ship_info.MMSI,
                    'Vessel_Name': ship_info.Vessel_Name,
                    'Total_Time_of_Berthing': strfdelta(total_time_in_port),
                    'Area': port.name,
                    'Length': ship_info.Length,
                    'Ship_Type': ship_info.Type 
                })

    result_df = pd.DataFrame(result_data)

    # Save the result DataFrame to a CSV file in the specified directory
    output_file_path = os.path.join(output_directory, 'ship_port_data.csv')
    result_df.to_csv(output_file_path, index=False, encoding='utf_8_sig', sep=';')

    print(f"Result data saved to: {output_file_path}")