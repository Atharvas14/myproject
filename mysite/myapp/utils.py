from math import sin, cos, sqrt, atan2, radians

def distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    # convert decimal degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # calculate the difference between the latitudes and longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # use the Haversine formula to calculate the distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance