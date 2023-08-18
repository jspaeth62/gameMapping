import pickle
import pandas as pd

# Load the pickle file containing the dictionary
with open('ncaafgames_dict.pickle', 'rb') as f:
    data_dict = pickle.load(f)

# Create an empty list to hold the dataframes
dataframes = []

# Iterate through the dictionary and append dataframes to the list
for df in data_dict.values():
    dataframes.append(df)

# Concatenate the list of dataframes into a single dataframe
merged_df = pd.concat(dataframes, ignore_index=True)

# Save the merged dataframe to a CSV file
merged_df.to_csv('merged_data.csv', index=False)
