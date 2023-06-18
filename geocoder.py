import googlemaps

gmaps = googlemaps.Client("AIzaSyAUu5mSd5dc5VdMJ3lrcvCDXY-SzaGZMas")


def get_coordinates(address):
    result = gmaps.geocode(address)
    if len(result) > 0:
        print(result)
        location = result[0]['geometry']['location']
        lat = location['lat']
        lon = location['lng']
        return lat, lon
    else:
        return None

'''
def main(address):
    coordinates = get_coordinates(address)

    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
    else:
        print("Geocoding was not successful.")
'''
