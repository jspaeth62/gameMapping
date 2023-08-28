import pandas as pd
#import googlemaps
#import plotly.graph_objects as go
import pickle
#from geopy.geocoders import Nominatim
#from geopy import exc
#import geopy.geocoders
#import plotly.express as px
#from plotly.subplots import make_subplots
#import folium
'''
# Read the Excel file
excel_file = 'C:/Users/Josh Spaeth/Desktop/projects/Game Mapping/stadiumAddresses.xlsx'
sheet1_name = 'NFL'
sheet2_name = 'NCAAF'

# Load both sheets into separate dataframes
NFL = pd.read_excel(excel_file, sheet_name=sheet1_name, skiprows=1)
NCAAF = pd.read_excel(excel_file, sheet_name=sheet2_name, skiprows=1)

# Initialize the Google Maps Geocoding client
api_key = 'AIzaSyBVfFU9xbtXZZKynPFYHarTPqL94LaUDL4'  # Replace with your own Google Maps Geocoding API key
gmaps = googlemaps.Client(key=api_key)

# Set a custom user agent
geopy.geocoders.options.default_user_agent = "my-application123"

def validate_address(address):

    try:
        geocode_result = gmaps.geocode(address)
    
        return geocode_result
    except:

        return False
'''
def validation(table):
# Test the validity of addresses in Table
    for address in table.iloc[:, 1]:
        is_valid = validate_address(address)
        print(f"Address: {address} | Valid: {is_valid}")

def get_geocode(address):

    geocode_result = validate_address(address)

    if geocode_result != False:
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng
    
    else:
        return 0, 0

def load_plot(table):
    lats = []
    lngs = []
    team_labels = []

    for team, address in zip(table['Team'], table['Stadium']):
        location = get_geocode(address)
        lat, lng = location
        lats.append(lat)
        lngs.append(lng)
        team_labels.append(team)
    
    return lats, lngs, team_labels

def create_plot(table1, table2):
    lats1, lngs1, team_labels1 = load_plot(table1)
    lats2, lngs2, team_labels2 = load_plot(table2)

    fig = go.Figure(data=go.Scattergeo(
    lon = lngs1,
    lat = lats1,
    mode = 'markers',
    marker = dict(size = 8, color = 'red'),
    text = team_labels1,
))

    fig.add_trace(go.Scattergeo(
        lon = lngs2,
        lat = lats2,
        mode = 'markers',
        marker = dict(size = 8, color = 'blue'),
        text = team_labels2))

    # Customize the layout
    fig.update_layout(
        title_text = 'Teams Map',
        showlegend = False,
        geo = dict(
            scope = 'usa',
            projection_type = 'albers usa',
            showland = True,
            landcolor = 'rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        )
    )

    fig.update_traces(hovertemplate='%{text}')
    fig.update_traces(hoverlabel=dict(namelength=0))

    # Display the plot
    fig.write_html('C:/Users/Josh Spaeth/Desktop/projects/Game Mapping/mapoutput.html')

def creategames():

    masterdict = {}

    dateslist = ['20231024', '20231031', '20231107', '20231114', '20231121', '20231128', '20231205', '20231212', '20231219', '20231226', '20240102', '20240109', '20240116', '20240123', '20240130', '20240206', '20240213', '20240220', '20240227', '20240305', '20240312', '20240319', '20240326', '20240402', '20240409']

    for i in range(len(dateslist)-1):
        # URL or HTML content of the page with table-like data
        url = 'https://www.espn.com/nba/schedule/_/date/' + dateslist[i]  # Replace with the actual URL or HTML content

        # Read HTML tables from the page
        tables = pd.read_html(url, header=0)

        # Assuming the desired table is the first one on the page
        #print(len(tables))

        runner = len(tables)

        for j in range(0,runner):
            table_data = tables[j]

            print(table_data)

            if 'TIME' in table_data.columns:
                table_data = table_data.rename(columns={'MATCHUP': 'AWAY TEAM'})
                table_data = table_data.rename(columns={'MATCHUP.1': 'HOME TEAM'})
                table_data = table_data.drop('TIME', axis=1)
                table_data = table_data.drop('TV', axis=1)
                table_data = table_data.drop('tickets', axis=1)
                #table_data = table_data.drop('Unnamed: 6', axis=1)
                table_data['HOME TEAM'] = table_data['HOME TEAM'].str[2:]

                # Ask the user for a date
                date = input("Enter the date: ")

                # Assign the entered date to the 'Date' column for all rows
                table_data['Date'] = date

                print(table_data)
            
            else:
                continue

                # Print the DataFrame with the dates
            masterdict[date] = table_data

                # Print the extracted table data
                #print(table_data)
        
    with open('nbagames_dict.pickle', 'wb') as file:
        pickle.dump(masterdict, file)

def readPickle(fileo):

    # To load the dictionary from the pickle file:
    with open(fileo, 'rb') as file:
        loaded_dict = pickle.load(file)
    
    return loaded_dict

def add_sport(dict):

    sport = input("Which sport? ")

    for df in dict.values():
        df['Sport'] = sport
    
    with open('ncaafgames_dict.pickle', 'wb') as file:
        pickle.dump(dict, file)

def extract_city(name):

    try:

        comma = name.find(',')
    
    except AttributeError:
        return None

    city = name[comma+2:]

    return city

def create_address_df(tables, path):

    cities = []
    lats = []
    longs = []

    for table in tables:

        stadiumlist = table['Location / Weather'].tolist()

        for stadium in stadiumlist:

            city = extract_city(stadium)

            if city != None:

                if city not in cities:
                    cities.append(city)
                    latitude, longitude = get_geocode(city)
                    lats.append(latitude)
                    longs.append(longitude)
                    
                else:
                    continue
            
            else:
                continue
    
    cities_df = pd.DataFrame({
        "City": cities,
        "Latitude": lats,
        "Longitude": longs
    })

    cities_df.to_csv(path)

def add_coords(games_dict):

    # Create "Latitude" and "Longitude" columns
    for value in games_dict.values():
        value["Latitude"] = None
        value["Longitude"] = None
    
    # Iterate through the dictionary and add latitude and longitude
    for key, value in games_dict.items():
        location = value["Location / Weather"]
        latitude, longitude = get_geocode(location)
        value["Latitude"] = latitude
        value["Longitude"] = longitude
    
    return games_dict

    #with open('ncaafgames_stadiums_dict.pickle', 'wb') as file:
        #pickle.dump(dict, file)

def main():
    #create_plot(NFL, NCAAF)

    #print(NCAAF['Team'])
    #load_plot(NFL)

    creategames()

    #NCAAFdictg = readPickle('ncaafgames_dict.pickle')

    #for table in NCAAFdictg.values():
        #print(table)
    #dict_coords = add_coords(NCAAFdictg)
    #NCAAFstadDictg = readPickle('ncaafgames_stadiums_dict.pickle')
    
    #excel_file1 = 'C:/Users/Josh Spaeth/Desktop/projects/Game Mapping/stadiumAddresses.xlsx'
    #sheet = "NCAAF"

    #NCAAFstadiums = pd.read_excel(excel_file1, sheet_name=sheet)

    #add_coords(NCAAFdictg, NCAAFstadiums)

    #NFLdictg = readPickle('nflgames_dict.pickle')

    #filepath = 'C:/Users/Josh Spaeth/Desktop/projects/Game Mapping/NCAAFcities.csv'

    #NCAAFstadiums = create_address_df(NCAAFdictg.values(), filepath)

    #print(get_geocode(address))
    #add_sport(NCAAFdictg)

    #create_slider(NFLdictg, NCAAFdictg)

main()
