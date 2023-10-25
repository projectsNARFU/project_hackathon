from datetime import datetime
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

    print("Расстояние от спутника до точки на карте:", distance, "километров")
    print("Азимут от спутника до точки на карте:", azimuth, "градусов\n")


class Satellite:

    def __init__(self, id, tle_line1, tle_line2):  # Метод инициализации
        self.id = id
        self.tle_line1 = tle_line1
        self.tle_line2 = tle_line2  # Установка значений атрибутов
        self.satellite = self.create_satellite()
        self.datetime = datetime.datetime.now()
        self.position, self.velocity = self.position_velocity()
        self.satellite_lat, self.satellite_lon = self.satellite_coordinates()

    def create_satellite(self):
        return twoline2rv(self.tle_line1, self.tle_line2, wgs72)

    # def parse_dat_time(self):
    #     return datetime.strptime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")

    def position_velocity(self):
        return self.satellite.propagate(self.datetime.year, self.datetime.month, self.datetime.day,
                                        self.datetime.hour, self.datetime.minute, self.datetime.second)

    def satellite_coordinates(self):
        satellite_lat = self.position[0]
        satellite_lon = self.position[1]
        return check_coordinates(satellite_lat, satellite_lon)

    def __str__(self):
        return f"{self.id}{self.tle_line1}{self.tle_line2}"


if __name__ == '__main__':
    with open("satellite.txt", 'r') as f:
        while True:
            id = f.readline()
            if not id:
                break
            tle_line1 = f.readline()
            tle_line2 = f.readline()
            st = Satellite(id, tle_line1, tle_line2)
            print(st)
            find_distance_azimuth(st.satellite_lat, st.satellite_lon)
    f.close()
