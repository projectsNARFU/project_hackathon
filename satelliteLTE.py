from datetime import datetime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from geopy.distance import great_circle
from geopy import Point
import math
import ast
# Данные о спутнике и даты и время
tle_line1 = "1 25544U 98067A   21153.29711597  .00001425  00000-0  32995-4 0  9999"
tle_line2 = "2 25544  51.6442  37.8222 0009500 307.6155  52.4418 15.49055797391289"
datetime_str = "2021-06-02 12:00:00"

# Разбор строки TLE
satellite = twoline2rv(tle_line1, tle_line2, wgs72)

# Парсинг даты и времени
date_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

# Вычисление координаты и скорости спутника в заданное время
position, velocity = satellite.propagate(date_time.year, date_time.month, date_time.day,
                                         date_time.hour, date_time.minute, date_time.second)

# Координаты спутника
satellite_lat = position[0]
satellite_lon = position[1]

# Координаты точки на карте
with open("choosed_coords.geojson", 'r') as f:
    info_coords = f.readline()
    info_coords = ast.literal_eval(info_coords)
f.close()
point_lat, point_lon = info_coords["coordinates"]
point_lat = int(point_lat)
point_lon = int(point_lon)



# Нормализация координат спутника, чтобы убедиться, что они находятся в правильном диапазоне
satellite_lat = max(min(satellite_lat, 90), -90)
satellite_lon = max(min(satellite_lon, 180), -180)

# Создайте объекты точек с координатами
satellite_point = Point(latitude=satellite_lat, longitude=satellite_lon)
point_on_map = Point(latitude=point_lat, longitude=point_lon)

# Вычислите расстояние между спутником и точкой
distance = great_circle(satellite_point, point_on_map).kilometers

# Вычислите азимут от спутника к точке
azimuth = math.degrees(math.atan2(math.sin(point_lon - satellite_lon), math.cos(satellite_lat) * math.tan(point_lat) - math.sin(satellite_lat) * math.cos(point_lon - satellite_lon)))

print("Расстояние от спутника до точки на карте:", distance, "километров")
print("Азимут от спутника до точки на карте:", azimuth, "градусов")
