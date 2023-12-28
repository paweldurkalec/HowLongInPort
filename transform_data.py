import os
import pandas as pd

def filter_corrupted_data(directory_path, new_directory_path, delimiter, encoding):
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)

            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path,sep=';',encoding='mbcs', low_memory=False)

            # Remove rows where the second or third column is empty
            df = df.dropna(subset=['Latitude', 'Longitude'])
            
            # Remove rows where the value of either the second or third column is "Not available (default)"
            df = df[~((df['~MMSI'] == '111111111') | (df['Latitude'] == 'Not available (default)') | (df['Longitude'] == 'Not available (default)'))]

            # Extract file name and extension from the file path
            file_name, file_extension = os.path.splitext(filename)

            # Construct the new file name with the 'new' prefix
            new_file_name = f'new_{file_name}{file_extension}'

            # Save the modified DataFrame to a new CSV file
            new_file_path = os.path.join(new_directory_path, new_file_name)
            df.to_csv(new_file_path, sep=delimiter, encoding=encoding, index=False)

            print(f"Filtered data saved to: {new_file_path}")

def merge_and_clean(directory_path, delimiter, encoding):
    # Initialize an empty list to store DataFrames
    df_list = []
    print(f"Merging data...\n")

    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            # Construct the full file path
            file_path = os.path.join(directory_path, filename)

            # Load the CSV file into a DataFrame
            df = pd.read_csv(file_path, sep=delimiter, encoding=encoding, low_memory=False)

            # Keep only the desired columns
            selected_columns = ['~MMSI', 'Vessel Name', 'Latitude', 'Longitude', 'Speed Over Ground (SOG)', 'Received Time UTC', 'Length', 'Ship Type']
            df = df[selected_columns]

            # Append the DataFrame to the list
            df_list.append(df)

    # Concatenate all DataFrames into a single DataFrame
    result_df = pd.concat(df_list, ignore_index=True)

    print(f"All data merged.\n")
    
    return result_df
