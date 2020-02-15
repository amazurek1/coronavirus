# Install first via terminal:  pip install overpy
# Code to get cities and their lattitude and longitude for selected countries
import csv
import json
import time

import overpy

iso_codes = {}
# Key is city name value is a list of country codes
cities = {}

# City coordinates - keys is City name
city_coords = {}

major_iso_codes = ['CN', 'TH', 'JP', 'SG',]
# major_iso_codes = ['AU', 'KR', 'MY', 'DE',]

# 'US', 'FR', 'VN', 'CA']


def read_iso_codes():
    global iso_codes

    with open('iso-codes.csv', mode='r') as infile:
        reader = csv.reader(infile)
        # Skip 2 header rows
        next(reader)
        next(reader)
        for r in reader:
            print(f"{r[3]} {r[0]}")
            iso_codes[r[3]] = r[0]


def get_cities_for_country(iso_code):
    global cities
    api = overpy.Overpass()

    query = f'area["ISO3166-1"="{iso_code}"][admin_level=2];node["place"="city"](area);out center;'

    r = api.query(query)
    time.sleep(15)
    # r = api.query("""
    # area["ISO3166-1"="US"][admin_level=2];
    # node["place"="city"](area);
    # out;
    # """)

    print(f"There are {len(r.nodes)} cities for {iso_code}")
    for n in r.nodes:
        print(f"Latitude: {n.lat} Longitude: {n.lon}")
        if 'name' in n.tags:
            if 'name:en' in n.tags:
                city = n.tags['name:en']
            else:
                city = n.tags['name']
            print(city)
            if city in cities:
                cities[city].append(iso_code)
            else:
                cities[city] = []
                cities[city].append(iso_code)

            if city not in city_coords:
                city_coords[city] = (float(n.lat), float(n.lon))
    return r


def main():
    read_iso_codes()
    print(iso_codes)

    for iso_code in major_iso_codes:
        print(f"Getting cities for {iso_code} country: {iso_codes[iso_code]}")
        get_cities_for_country(iso_code)

    # print(cities)

    with open('cities.json', 'w') as fp:
        json.dump(cities, fp, indent=4)

    with open('cities_coords.json', 'w') as fp:
        json.dump(city_coords, fp, indent=4)


main()


if False:
    get_cities_for_country('BH')
    with open('cities.json', 'w') as fp:
        json.dump(cities, fp, indent=4)

    with open('cities_coords.json', 'w') as fp:
        json.dump(city_coords, fp, indent=4)
