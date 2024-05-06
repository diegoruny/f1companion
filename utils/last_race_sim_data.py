import pandas as pd

# Load datasets
drivers_df = pd.read_csv('./api/localData/drivers.csv')
results_df = pd.read_csv('./api/localData/results.csv')
constructors_df = pd.read_csv('./api/localData/constructors.csv')
races_df = pd.read_csv('./api/localData/races.csv')
circuits_df = pd.read_csv('./api/localData/circuits.csv')
qualifying_df = pd.read_csv('./api/localData/qualifying.csv')

# Merging data
race_details_df = pd.merge(results_df, drivers_df, on='driverId', how='left')
race_details_df = pd.merge(race_details_df, constructors_df[['constructorId', 'constructorRef', 'name']], on='constructorId', how='left', suffixes=('', '_constructor'))
race_details_df = pd.merge(race_details_df, races_df, on='raceId', how='left')
race_details_df = pd.merge(race_details_df, circuits_df, on='circuitId', how='left')
race_details_df = pd.merge(race_details_df, qualifying_df, on=['raceId', 'driverId', 'constructorId'], how='left')

# Resolve constructorId conflicts
race_details_df['constructorId'] = race_details_df['constructorId_x'].fillna(race_details_df['constructorId_y'])
race_details_df.drop(['constructorId_x', 'constructorId_y'], axis=1, inplace=True)

# Selecting relevant columns, ensuring correct constructorId is used
columns_to_select = ['raceId', 'driverId', 'code', 'surname', 'constructorId', 'constructorRef', 'name', 'grid', 'positionOrder', 'points', 'circuitRef', 'location', 'country', 'lat', 'lng']
race_details_df = race_details_df[columns_to_select]

# Print to verify the final structure
print("Final DataFrame columns:", race_details_df.columns)
print(race_details_df.head())
