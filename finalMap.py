import pandas as pd
import folium
import requests
import ipywidgets as widgets
from IPython.display import display

# Read spreadsheet data
file_path = 'merged_data.xlsx'
df = pd.read_excel(file_path, sheet_name=None)

# Google Maps API key
api_key = 'AIzaSyBVfFU9xbtXZZKynPFYHarTPqL94LaUDL4'

# Create a map
m = folium.Map(location=[40, -100], zoom_start=4)

# Function to get latitude and longitude from address using Google Maps API
def get_lat_lon(address):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': address, 'key': api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    location = data['results'][0]['geometry']['location']
    return location['lat'], location['lng']

# Function to update map based on user input
def update_map(date_range, selected_sports):
    m.clear_layers()  # Clear existing markers
    for sport, data in df.items():
        if sport in selected_sports:
            filtered_data = data[(data['Date'] >= date_range[0]) & (data['Date'] <= date_range[1])]
            for index, row in filtered_data.iterrows():
                address = row['Address']
                lat, lon = get_lat_lon(address)
                folium.Marker([lat, lon], popup=row['Home Team']).add_to(m)
    
    # Save the map to an HTML file
    m.save('interactive_map.html')

# Create interactive widgets
start_date_slider = widgets.DatePicker(description='Start Date')
end_date_slider = widgets.DatePicker(description='End Date')
sports_checkboxes = widgets.SelectMultiple(options=list(df.keys()), description='Sports')

# Create an output widget for the map
map_output = widgets.Output()

# Define a function to handle widget interaction
def handle_interaction(change):
    date_range = (start_date_slider.value, end_date_slider.value)
    selected_sports = sports_checkboxes.value
    with map_output:
        update_map(date_range, selected_sports)
        display(m)

# Attach the interaction function to the widget events
start_date_slider.observe(handle_interaction, names='value')
end_date_slider.observe(handle_interaction, names='value')
sports_checkboxes.observe(handle_interaction, names='value')

# Display widgets and map
widgets_box = widgets.VBox([start_date_slider, end_date_slider, sports_checkboxes])
display(widgets_box, map_output)
