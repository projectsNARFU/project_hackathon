import pickle
from datetime import datetime
from class_serialize import Persistence_Exemplar as PE
import requests
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from geopy.distance import great_circle
from geopy import Point
import math
import ast
import datetime


def check_coordinates(satellite_lat, satellite_lon):
    return max(min(satellite_lat, 90), -90), max(min(satellite_lon, 180), -180)


def take_geojson_coordinates():
    # Координаты точки на карте
    with open("choosed_coords.geojson", 'r') as f:
        info_coords = f.readline()
        info_coords = ast.literal_eval(info_coords)
    f.close()
    point_lat, point_lon = info_coords["coordinates"]
    point_lat = int(point_lat)
    point_lon = int(point_lon)
    return point_lat, point_lon


def count_azimuth(point_lon, point_lat, satellite_lon, satellite_lat):
    return math.degrees(math.atan2(math.sin(point_lon - satellite_lon),
                                   math.cos(st.satellite_lat) * math.tan(point_lat) - math.sin(
                                       satellite_lat) * math.cos(point_lon - satellite_lon)))


def create_point(lat, lon):
    return Point(latitude=lat, longitude=lon)


def find_distance_azimuth(satellite_lat, satellite_lon):
    point_lat, point_lon = take_geojson_coordinates()

    # Создаем объекты точек с координатами
    satellite_point = create_point(satellite_lat, satellite_lon)
    point_on_map = create_point(point_lat, point_lon)

    # Вычисляем расстояние между спутником и точкой
    distance = great_circle(satellite_point, point_on_map).kilometers

    # Вычисляем азимут от спутника к точке
    azimuth = count_azimuth(point_lon, point_lat, satellite_lon, satellite_lat)
    return distance, azimuth
    # print("Расстояние от спутника до точки на карте:", distance, "километров")
    # print("Азимут от спутника до точки на карте:", azimuth, "градусов\n")


class Satellite:
    satellites = []

    def __init__(self, id, tle_line1, tle_line2):  # Метод инициализации
        self.id = id
        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2  # Установка значений атрибутов
        self.satellite = self.create_satellite()
        self.datetime = datetime.datetime.now()
        self.position, self.velocity = self.position_velocity()
        self.satellite_lat, self.satellite_lon = self.satellite_coordinates()
        self.satellites.append(self)

    def serialize(self):
        with open('satellites.pkl', 'wb') as f:
            pickle.dump(self.satellites, f)
        f.close()

    @staticmethod
    def deserialize():
        try:
            with open('satellites.pkl', 'rb') as f:
                satellites = pickle.load(f)
        except FileNotFoundError:
            print("File isn't found")
        return satellites

    def create_satellite(self):
        return twoline2rv(self.tle_line1, self.tle_line2, wgs72)


    def position_velocity(self):
        return self.satellite.propagate(self.datetime.year, self.datetime.month, self.datetime.day,
                                        self.datetime.hour, self.datetime.minute, self.datetime.second)

    def satellite_coordinates(self):
        satellite_lat = self.position[0]
        satellite_lon = self.position[1]
        return check_coordinates(satellite_lat, satellite_lon)

    def __str__(self):
        return f"{self.id}\n{self.tle_line1}\n{self.tle_line2}"


def parse_info():
    url = 'http://eostation.scanex.ru/schedule/tle/new.tle'
    response = requests.get(url)
    satellite_list = []
    if response.status_code == 200:
        str_list = response.content.decode("utf-8")

        # for line in str_list:
        #     if line.startswith("\n"):
        #         satellite_list.append(line)
        return str_list
    else:
        print("error", response.status_code)


def show_satellite(find_id):
    data = Satellite.deserialize()
    for satellite in data:
        if satellite.id == find_id:
            print(satellite)


if __name__ == '__main__':
    closest_id = None
    min_distance = float('inf')
    closest_azimuth = 181


    not_split_lines = parse_info()
    lines = not_split_lines.split("\r\n")
    last_info_update = lines[0]
    lines = lines[:-1]

    for i in range(1, len(lines) - 2, 3):
        id = lines[i]
        tle_line1 = lines[i + 1]
        tle_line2 = lines[i + 2]
        st = Satellite(id, tle_line1, tle_line2)
        print(st)

        st.serialize()
        distance, azimuth = find_distance_azimuth(st.satellite_lat, st.satellite_lon)
        print("Расстояние от спутника до точки на карте:", distance, "километров")
        print("Азимут от спутника до точки на карте:", azimuth, "градусов\n")
        if distance < min_distance:
            min_distance = distance
            closest_id = id
        elif distance == min_distance:
            if abs(azimuth) < abs(closest_azimuth):
                closest_azimuth = azimuth
                closest_id = id
        # data = Satellite.deserialize()
        # for satellite in data:
        #     print(satellite.id)

    show_satellite('TM-0102')

    print(f"\n\nClosest satellite: {closest_id} Minimum Distance: {min_distance} kilometers\n" \
          f"Minimum Azimuth: {closest_azimuth} degrees ")
