import json
import ast


def create_coords(info_coords):
    with open("choosed_coords.geojson", 'w') as f:
        f.write(json.dumps(info_coords))
    f.close()


def input_coords():
    """вводим координаты местности"""
    coords = input("введите координаты в формате: широта долгота")
    coords = coords.replace(',', '')
    coords = coords.split()

    info_coords = {"coordinates": coords, "type": "Point"}
    create_coords(info_coords)


if __name__ == '__main__':
    input_coords()

    with open("choosed_coords.geojson", 'r') as f:
        info_coords = f.readline()
        info_coords = ast.literal_eval(info_coords)
    f.close()
