import json
from geojson import Point


def create_coords(info_coords):
    with open("choosed_coords.geojson", 'w') as f:
        f.write(json.dumps(info_coords))

def save_coords(info_coords):
    with open("choosed_coords.geojson", 'wb') as f:
        pass

def input_coords():
    """вводим координаты местности"""
    coords = input()
    coords = coords.replace(',', '')
    coords = coords.split()

    info_coords = {"coordinates": coords, "type": "Point"}

    create_coords(info_coords)
    # try:
    #     create_coords(coords)
    # except:
    #     save_coords(coords)


if __name__ == '__main__':
    input_coords()

