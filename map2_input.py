import folium
import requests

PATH = 'https://us1.locationiq.com/v1/search.php' 
LOCATIONIQ_API_KEY = 'pk.1f00c7cb204323568c51950910d520e8' 

map = folium.Map([38.58, -99.09], zoom_start=6, tiles="Stamen Terrain")
coord_dict = {} # key is place, value is coordinates (tuple w/ floats)
fg_w = folium.FeatureGroup(name="Wishlist")

def get_place_from_user():
    place = input("Where would you like to visit? ")
    return place.lower().capitalize()

def get_response(place):
    query_params = {
        "key": LOCATIONIQ_API_KEY,
        "q": place,
        "format": "json"
    }
    return requests.get(PATH, params=query_params)

def get_lat_lon(response):
    return (float(response[0]["lat"]), float(response[0]["lon"]))
    

def add_to_wishlist():
    while True:
        # assume all places will get a proper response
        place = get_place_from_user()
        response = get_response(place)
        response_body = response.json()
        coord_dict[place] = get_lat_lon(response_body)

        quit = input("Do you want to continue? (y for yes, anything else to quit): ")
        if quit.lower() != "y":
            break

add_to_wishlist()

for place in coord_dict:
    fg_w.add_child(folium.CircleMarker(location=coord_dict[place],
    popup=place, fill_color="blue", fill_opacity=0.8, color="grey"))

map.add_child(fg_w)
map.save("Map2.html") # this is what will create the file and update it

# # POPULATION LAYER
# # this could be done w/o FeatureGroup, must do map.add_child...
# fg_p = folium.FeatureGroup(name="Population")
# fg_p.add_child(folium.GeoJson(data=open("Webmap_datasources/world.json", "r", encoding="utf-8-sig").read(), 
# style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
# else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

# # add to map first
# map.add_child(fg_v)
# map.add_child(fg_p)

# # then add controls for layers (filters), if desired
# map.add_child(folium.LayerControl()) 
# map.save("Map1.html")