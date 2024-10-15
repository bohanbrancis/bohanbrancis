import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime

connection = sqlite3.connect('ufc_crawl/ufc_data.db')

# Query to select all data from the specified table
query_01 = f"SELECT * FROM {'ufc_fights'};"
query_02 = f"SELECT * FROM {'ufc_fighters'};"

# Use pandas to read data from the SQLite database into a DataFrame
ufc_fights = pd.read_sql_query(query_01, connection)
ufc_fighters = pd.read_sql_query(query_02, connection)
# Close the connection
connection.close()

ufc_fights['Date'] = pd.to_datetime(ufc_fights['Date'])


ufc_fighters['DOB'] = pd.to_datetime(ufc_fighters['DOB'], errors='coerce')
ufc_fighters[['Wins','Losses', 'Draws(NC)']] = ufc_fighters.Record.str.split('-',expand=True)
ufc_fighters['Wins'] = pd.to_numeric(ufc_fighters['Wins'].str.replace('Record: ', ''), errors='coerce')
ufc_fighters['Losses'] = pd.to_numeric(ufc_fighters['Losses'], errors='coerce')

ufc_fighters['Weight'] = pd.to_numeric(ufc_fighters['Weight'].str.replace(' lbs', ''), errors='coerce')
ufc_fighters['Reach'] = pd.to_numeric(ufc_fighters['Reach'].str.replace('"', ''), errors='coerce')
ufc_fighters['Sig_Str_Acc'] = pd.to_numeric(ufc_fighters['Sig_Str_Acc'].str.replace('%',''), errors='coerce')
ufc_fighters['Sig_Str_Acc'] = ufc_fighters['Sig_Str_Acc'] / 100
ufc_fighters['Str_Def'] = pd.to_numeric(ufc_fighters['Str_Def'].str.replace('%',''), errors='coerce')
ufc_fighters['Str_Def'] = ufc_fighters['Str_Def'] / 100
ufc_fighters['TD_Acc'] = pd.to_numeric(ufc_fighters['TD_Acc'].str.replace('%',''), errors='coerce')
ufc_fighters['TD_Acc'] = ufc_fighters['TD_Acc'] / 100
ufc_fighters['TD_Def'] = pd.to_numeric(ufc_fighters['TD_Def'].str.replace('%',''), errors='coerce')
ufc_fighters['TD_Def'] = ufc_fighters['TD_Def'] / 100
ufc_fighters['Sig_Str_Abs_M'] = pd.to_numeric(ufc_fighters['Sig_Str_Abs_M'], errors='coerce')
ufc_fighters['Sig_Str_M'] = pd.to_numeric(ufc_fighters['Sig_Str_M'], errors='coerce')
ufc_fighters['TD_Avg'] = pd.to_numeric(ufc_fighters['TD_Avg'], errors='coerce')
ufc_fighters['Sub_Avg'] = pd.to_numeric(ufc_fighters['Sub_Avg'], errors='coerce')


def height_to_inches(height):
    parts = height.split("'")
    feet = int(parts[0].strip()) if len(parts) > 0 and parts[0].strip().isdigit() else 0  # Extract feet if it's a valid number, otherwise set to 0
    inches = 0  # Default value for inches

    # Check if there is a valid inches part in the height string
    if len(parts) > 1:
        inches_part = parts[1].replace('"', '').strip()
        if inches_part and inches_part.isdigit():
            inches = int(inches_part)  # Convert inches to int if it's a valid number

    total_inches = feet * 12 + inches
    return total_inches

def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = minutes * 60 + seconds
        return total_seconds
    except (ValueError, AttributeError):
        return np.nan  # Set invalid or missing values to NaN



ufc_fights['f1_CTRL'] = ufc_fights['f1_CTRL'].apply(time_to_seconds)
ufc_fights['f2_CTRL'] = ufc_fights['f2_CTRL'].apply(time_to_seconds)
ufc_fighters['Height'] = ufc_fighters['Height'].apply(height_to_inches)

ufc_fights['Round'] = pd.to_numeric(ufc_fights['Round'], errors='coerce')
ufc_fights['F1KD'] = pd.to_numeric(ufc_fights['F1KD'], errors='coerce')
ufc_fights['F2KD'] = pd.to_numeric(ufc_fights['F2KD'], errors='coerce')
ufc_fights['f1_Sig_STR_pct'] = pd.to_numeric(ufc_fights['f1_Sig_STR_pct'].str.replace('%',''), errors='coerce')
ufc_fights['f1_Sig_STR_pct'] = ufc_fights['f1_Sig_STR_pct'] / 100

ufc_fights['f2_Sig_STR_pct'] = pd.to_numeric(ufc_fights['f2_Sig_STR_pct'].str.replace('%',''), errors='coerce')
ufc_fights['f2_Sig_STR_pct'] = ufc_fights['f2_Sig_STR_pct'] / 100


ufc_fights['f1_TD_pct'] = pd.to_numeric(ufc_fights['f1_TD_pct'].str.replace('%',''), errors='coerce')
ufc_fights['f1_TD_pct'] = ufc_fights['f1_TD_pct'] / 100

ufc_fights['f2_TD_pct'] = pd.to_numeric(ufc_fights['f2_TD_pct'].str.replace('%',''), errors='coerce')
ufc_fights['f2_TD_pct'] = ufc_fights['f2_TD_pct'] / 100

ufc_fights['f1_Sub_ATT'] = pd.to_numeric(ufc_fights['f1_Sub_ATT'], errors='coerce')
ufc_fights['f2_Sub_ATT'] = pd.to_numeric(ufc_fights['f2_Sub_ATT'], errors='coerce')
ufc_fights['f1_Rev'] = pd.to_numeric(ufc_fights['f1_Rev'], errors='coerce')
ufc_fights['f2_Rev'] = pd.to_numeric(ufc_fights['f2_Rev'], errors='coerce')

ufc_fights[['f1_Landed_Sig_STR', 'f1_Thrown_sig_STR']] = ufc_fights['f1_Sig_STR'].str.extract(r'(\d+) of (\d+)')

# Convert the extracted columns to numeric values
ufc_fights['f1_Landed_Sig_STR'] = pd.to_numeric(ufc_fights['f1_Landed_Sig_STR'])
ufc_fights['f1_Thrown_sig_STR'] = pd.to_numeric(ufc_fights['f1_Thrown_sig_STR'])


ufc_fights[['f2_Landed_Sig_STR', 'f2_Thrown_sig_STR']] = ufc_fights['f2_Sig_STR'].str.extract(r'(\d+) of (\d+)')

# Convert the extracted columns to numeric values
ufc_fights['f2_Landed_Sig_STR'] = pd.to_numeric(ufc_fights['f2_Landed_Sig_STR'])
ufc_fights['f2_Thrown_sig_STR'] = pd.to_numeric(ufc_fights['f2_Thrown_sig_STR'])


ufc_fights[['f1_Landed_total_STR', 'f1_Thrown_total_STR']] = ufc_fights['f1_total_STR'].str.extract(r'(\d+) of (\d+)')

# Convert the extracted columns to numeric values
ufc_fights['f1_Landed_total_STR'] = pd.to_numeric(ufc_fights['f1_Landed_total_STR'])
ufc_fights['f1_Thrown_total_STR'] = pd.to_numeric(ufc_fights['f1_Thrown_total_STR'])

ufc_fights[['f2_Landed_total_STR', 'f2_Thrown_total_STR']] = ufc_fights['f2_total_STR'].str.extract(r'(\d+) of (\d+)')

# Convert the extracted columns to numeric values
ufc_fights['f2_Landed_total_STR'] = pd.to_numeric(ufc_fights['f2_Landed_total_STR'])
ufc_fights['f2_Thrown_total_STR'] = pd.to_numeric(ufc_fights['f2_Thrown_total_STR'])

ufc_fights[['f1_Landed_TD', 'f1_Attempt_TD']] = ufc_fights['f1_TD'].str.extract(r'(\d+) of (\d+)')

# Convert the extracted columns to numeric values
ufc_fights['f1_Landed_TD'] = pd.to_numeric(ufc_fights['f1_Landed_TD'])
ufc_fights['f1_Attempt_TD'] = pd.to_numeric(ufc_fights['f1_Attempt_TD'])

ufc_fights[['f2_Landed_TD', 'f2_Attempt_TD']] = ufc_fights['f2_TD'].str.extract(r'(\d+) of (\d+)')

# Convert the extracted columns to numeric values
ufc_fights['f2_Landed_TD'] = pd.to_numeric(ufc_fights['f2_Landed_TD'])
ufc_fights['f2_Attempt_TD'] = pd.to_numeric(ufc_fights['f2_Attempt_TD'])

ufc_fighters.to_csv('ufc_fighters.csv')
ufc_fights.to_csv('ufc_fights.csv')