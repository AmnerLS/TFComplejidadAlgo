from math import radians, cos, sin, sqrt, atan2

class Haversine:
    def __init__(self):
        self.R = 6371.0

    def haversine(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = self.R * c
        return distance

    def get_distance(self, lat1, lon1, lat2, lon2):
        return self.haversine(lat1, lon1, lat2, lon2)