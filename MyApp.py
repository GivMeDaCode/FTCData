import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

uploaded_file = st.file_uploader("Choose a file")

df = None  # Initialize df outside the block

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter = "\t")


    # Perform operations on the dataframe
    #df = dataframe.copy()
    df = df.reset_index()
    df['refuel_flag'] = 'F'
    st.write(df.columns)
    df['TotalDistance'] = df['TotalDistance'] * 5
    df['TotalDistance'] = df['TotalDistance'] * 5
    df['TotalFuel'] = df['TotalFuel'] * 0.001
    df['TotalHours'] = df['TotalHours'] * 0.05
    df['FuelRate'] = df['FuelRate'] * 0.05
    df['EngineRPM'] = df['EngineRPM'] * 0.125
    df['CombinationWeight'] = df['CombinationWeight'] * 10
    df['FuelLevel'] = df['FuelLevel'] * 0.4

# Continue with the rest of your code
# Make sure all operations on df are within this if-else block

if df is not None:
    df = df.sort_values(['TripId', 'LoggedAt'], ascending=[True, True])

df = df.reset_index()
for i in range(len(df.index)-1):
    if((df.TripId[i] == df.TripId[i+1]) and ((df.FuelLevel[i+1] - df.FuelLevel[i]) > 15)):
        df.refuel_flag[i+1] = 'T'

df_2_trips = df[['CvdId', 'TripId', 'Fuel', 'FuelIdle', 'Distance', 'TripTime', 'TripIdleTime']]
df_2_trip_data = df[['TripId', 'Id', 'CvdId','LoggedAt', 'LocalTime', 'Speed', 'Heading', 'Direction', 'PDop', 'HDop', 'WeightKg', 'Latitude', 'Longitude', 'PTO', 'TotalFuel', 'TotalDistance', 'TotalHours', 'FuelLevel', 'FuelRate', 'CurrentGear','SerialNumber','EngineRPM','CombinationWeight', 'refuel_flag']]
df_2_vehicles = df[['CvdId', 'Vin', 'Nickname', 'Rego', 'Make', 'Description', 'Name']]

df_2_trips = df_2_trips.rename(columns={'TripId': 'Id'})
df_2_vehicles = df_2_vehicles.rename(columns={'Description': 'Model'})
df_2_vehicles = df_2_vehicles.rename(columns={'Name': 'Customer'})

df_2_trip_data['LoggedAt'] = df_2_trip_data['LoggedAt'].astype('datetime64[ns]')
df_2_trip_data['LocalTime'] = df_2_trip_data['LocalTime'].astype('datetime64[ns]')

df_2_trips = df_2_trips.drop_duplicates(subset=['Id'])
df_2_trip_data = df_2_trip_data.drop_duplicates(subset=['Id'])
df_2_vehicles = df_2_vehicles.drop_duplicates(subset=['CvdId'])

df_2_trip_data = df_2_trip_data[df_2_trip_data.TotalFuel != 4294967295]

df_2_trip_data.loc[df_2_trip_data['FuelLevel'] > 100, 'FuelLevel'] = 100

#df_2_trips.to_csv('Goldstar_Trips.csv',index=False)
#df_2_trip_data.to_csv('Goldstar_Trip_Data.csv',index=False)
#df_2_vehicles.to_csv('Goldstar_Vehicles.csv',index=False)

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df_2_trips)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Goldstar_Trips.csv',
    mime='text/csv',
)

csv = convert_df(df_2_trip_data)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Goldstar_Trip_Data.csv',
    mime='text/csv',
)

csv = convert_df(df_2_vehicles)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='Goldstar_Vehicles.csv',
    mime='text/csv',
)

