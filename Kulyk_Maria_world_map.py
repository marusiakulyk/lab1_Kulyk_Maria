import folium
import pandas
from geopy.geocoders import Nominatim


def csv_file(path):
    """
    THis function reads file and turns it into csv file
    """
    with open(path, encoding="utf-8", errors="ignore") as f:
        lst = [list(filter(lambda x: x != '', line.strip().split("\t"))) for line in f]
    lst = lst[15:-2]
    a = {"year": [i[0][i[0].index("(") + 1:i[0].index(")")] for i in lst],
         "film": [i[0][:i[0].index("(") - 1] for i in lst],
         "country": [i[1] for i in lst]
         }
    d = pandas.DataFrame(a, columns=["year", "film", "country"])
    return d


def adding_marker(feature_group, location, popup):
    """
    This function adds marker on a map

    """
    geolocator = Nominatim()
    location1 = geolocator.geocode(location)
    feature_group.add_child(folium.Marker(location=[location1.latitude, location1.longitude],
                               popup=popup,
                               icon=folium.Icon()))


# csv_file(read_file("locations.list"))


def main(year):
    year = int(input("Enter films of which year you want to see:"))
    number = int(input("Enter how many markers you want to see:"))
    f = csv_file("locations.list")
    map = folium.Map(location=[48.314775, 25.082925],
                     zoom_start=1)

    # creating a layer with film markers
    fg = folium.FeatureGroup(name="Population")
    k = 0
    for i in range(len(f)):
        if k == number:
            break
        try:
            a = int(f.ix[i, 'year'])
            if a == year:
                print(f.ix[i, 'country'])
                try:
                    adding_marker(fg, f.ix[i, 'country'], f.ix[i, 'film'])
                    k += 1
                except AttributeError:
                    pass
        except ValueError:
            continue
    map.add_child(fg)

    # creating a layer with population
    fg1 = folium.FeatureGroup(name="Population")
    fg1.add_child(folium.GeoJson(data=open('world.json',
                                           encoding='utf-8-sig').read(),
                                 style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 10000000
                                 else "orange" if 10000000 <= x["properties"]["POP2005"] < 20000000
                                 else "red"}))
    map.add_child(fg1)

    map.add_child(folium.LayerControl())
    map.save("Map_5.html")


main(1920)
